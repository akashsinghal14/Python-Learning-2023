from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
## All above are the selenium drivers

import os # to delete and do other thing path related
import yaml # to take input from other files
import time # to add wait time while browser loading or downloading 
import sys # to ask for cmd line arguments when executing
import git # to execute GIT related comands


# Take the input of content group while executing
#   Example:- .\login.py SR # will download the studnet readiness file
#   Example:- .\login.py RA # will download the Risk analysis file
cg = sys.argv
# print(cg)
cg = cg[1]


## This is the function to clean all files before starting any downloading from portal
def delete(path):
    allfiles = os.listdir(path)
    for i in range(len(allfiles)):
        if allfiles[i] == 'renamecg.py' or allfiles[i] == 'delcg.py':
            print("not going to delete this- "+ path+"\\"+allfiles[i])
        else:
            os.remove(path+"\\"+allfiles[i]) 

## Add all paths here
loginLink = "https://gtdev1-dev.hoonuit.com/Dashboard/login/login.jsp" # Login versifit link it could be gtdev or ps3 but this code is only tested for gtdev
migrationWindow="https://gtdev1-dev.hoonuit.com/Dashboard/page.portal?handler=CONTENT&_form_Action=open&_form_LinkId=1708&_form_Refresh=N&_rCacheSeed=1674627437694"  # link to open migration tool
downloadPath = "C:\\Users\\singhala\\Downloads\\RenameCG\\" # This is argumeent in two function delete and rename

# Importing details from other yml files
conf = yaml.safe_load(open('logindetails.yml'))
myUser = conf['versifit_user']['email']
myPassword = conf['versifit_user']['password']
# Below is the function which will go to migrtion tool and export the CG's
def login(url,usernameId, username, passwordId, password, submit_buttonId, contentgroup):

    # options = webdriver.ChromeOptions() 

    # Initiating driver to handle automatically using library
    chrome_options = webdriver.ChromeOptions()
    # Changing the downalod directory
    chrome_options.add_experimental_option("prefs", {"download.default_directory": downloadPath})
    driver = webdriver.Chrome(options=chrome_options)
    ## Open the link and login in gtdev
    driver.get(url)
    ## Maximize the window, its optional
    # driver.maximize_window()
    
    # parent = driver.current_window_handle         # Since multiple windows could open in this code so this line will help to know which one is at current being used
    # print(f"This is parent window : {parent}")

    ## Type cred and hit login button
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.ID, submit_buttonId).click()
    ## once logged in go to Migratino App from below
    driver.get(migrationWindow)
    ## changing the frames to checklist the options
    driver.switch_to.frame("migrationsource")
    driver.switch_to.frame("migrationOptions_Frame")
    ## check/uncheck the options for exporting CG
    driver.find_element(By.ID, "ExportChildren").click()
    driver.find_element(By.ID, "ExportToFile").click()
    driver.find_element(By.ID, "IncludeSecurity").click()

    ## Switch to main/parent frame
    driver.switch_to.default_content()
    ## Again swtich to main/parent frame
    driver.switch_to.default_content()
    ## Switch to new frames one by one
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
    driver.switch_to.frame("folderList")
    driver.switch_to.frame("NavTreeFrame")
    
    ## Click to expand content defintions
    driver.find_element(By.ID, "ip_MainNavTree45").click()

    ## using try and catch finding 
    try:
        ## Click to expand Content Groups
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ip_MainNavTree3492"))
        )
        element.click()
        
        ## Download Student Readiness CG
        if contentgroup == 'SR':
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree7077")))
            element.click()
            driver.switch_to.default_content()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
            driver.switch_to.frame("folderList")
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/a/table/tbody/tr/td/div/span/img"))
            )
            element.click()

            ## Above click will open a new tab so only new tab should be closed after downlaoding 
            exportwindow = driver.window_handles
            driver.switch_to.window(exportwindow[-1])
            time.sleep(10)
            driver.close()
            time.sleep(5)

        ## Download Student Readiness Interventions Beta
        elif contentgroup == 'IB':
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree7530")))
            element.click()
            driver.switch_to.default_content()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
            driver.switch_to.frame("folderList")
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/a/table/tbody/tr/td/div/span/img"))
            )
            element.click()
            
            ## Above click will open a new tab so only new tab should be closed after downlaoding 
            exportwindow = driver.window_handles
            driver.switch_to.window(exportwindow[-1])
            time.sleep(10)
            driver.close()
            time.sleep(5)
        else:
            exit() 


    finally:
        driver.quit()


def rename(path):
    allfiles = os.listdir(path)
    for x in range(len(allfiles)):
        firstfile = allfiles[x]
        ac_name = firstfile.split('_')
        if len(ac_name)>1:
            os.rename(path+"\\"+firstfile,path+"\\"+ac_name[1]+'.7z')

def gitpull(git_dir):
    g = git.cmd.Git(git_dir)
    g.pull()
    path = "C:\\Users\\singhala\\Downloads\\RenameCG\\"
    allfiles = os.listdir(path)
    # print(allfiles)
    for x in range(len(allfiles)-1):
        firstfile = allfiles[x]
        # print(firstfile)
        if firstfile=="InterventionsBeta.7z":
            os.replace("C:\\Users\\singhala\\Downloads\\RenameCG\\InterventionsBeta.7z", "C:\\Users\\singhala\\Documents\\Versift GIT Oct2021\\content-groups\\optional\\InterventionsBeta.7z")
        # else:
        #     exit()

# "C:\\Users\\singhala\\Documents\\Versift GIT Oct2021\\content-groups\\optional\\"
#calling functions 

## Take pull as well from GIT

# delete(downloadPath)
login(loginLink, "user", myUser, "pass", myPassword, "btnSubmit", cg)
# rename(downloadPath)
# gitpull("C:\\Users\\singhala\\Documents\\Versift GIT Oct2021\\content-groups\\")
