######################################################
# Below are the arguments and full form can be       #
# passed while executing the script, its required    #
# to pass at least one argument currently            #
#    1. IB = InterventionnsBeta                      #
#    2. SR = StudentReadiness                        #
#    3. ESS = Essentials                             #
#    4. AS = Assessment                              #
#    5. DL = DigitalLearning                         #
#    6. RA = RiskAnalysis                            #
#    7. SV = SystemAndVariables                      #
# Example: python .\login_multiple.py RA SV DL       #    
######################################################


## All below are the selenium drivers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions

import os # to delete and do other thing path related
import yaml # to take input from other files
import time # to add wait time while browser loading or downloading 
import sys # to ask for cmd line arguments when executing
import git # to execute GIT related comands
from dotenv.main import load_dotenv # to load .env file

## Import values from .env file
load_dotenv()
myUser = os.getenv('email')
myPassword = os.getenv('password')
loginLink = os.getenv('loginLink')
migrationWindow = os.getenv('migrationWindow')
downloadPath = os.getenv('downloadPath')
gitPath = os.getenv('gitPath')

# Take the input of content group while executing
cg = sys.argv
#   Example:- .\login.py SR # will download the studnet readiness file
#   Example:- .\login.py RA # will download the Risk analysis file

# All selenium variables
xpath_to_click_export='/html/body/div/table/tbody/tr[1]/td/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/a/table/tbody/tr/td/div/span/img'

## This is the function to clean all files before starting any downloading from portal
def delete(path):
    allfiles = os.listdir(path)
    for i in range(len(allfiles)):
            os.remove(path+"\\"+allfiles[i]) 

# ## Add all paths here
# # Login versifit link it could be gtdev or ps3 but this code is only tested for gtdev
# loginLink = "https://gtdev1-dev.hoonuit.com/Dashboard/login/login.jsp"
# # link to open migration tool
# migrationWindow="https://gtdev1-dev.hoonuit.com/Dashboard/page.portal?handler=CONTENT&_form_Action=open&_form_LinkId=1708&_form_Refresh=N&_rCacheSeed=1674627437694"
# # This is argumeent in two function delete and rename
# downloadPath = "C:\\Users\\singhala\\Downloads\\RenameCG\\"
# # Add your git path like below
# gitPath = "C:\\Users\\singhala\\Documents\\Versift GIT Oct2021\\content-groups\\"

# Importing details from other yml files
# conf = yaml.safe_load(open('logindetails.yml'))
# myUser = conf['versifit_user']['email']
# myPassword = conf['versifit_user']['password']

# Below is the function which will go to migrtion tool and export the CG's
def login(url,usernameId, username, passwordId, password, submit_buttonId, contentgroup):
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

    # initializing a variable to iterate on multiple CG download
    index=1

    ## using try and catch finding 
    try:
        ## Click to expand Content Groups
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ip_MainNavTree3492"))
        )
        element.click()
        #initializing the variable to monitor the downloading files
        i=0
        while index < len(cg):
            contentgroup = cg[index]
            ## Download Student Readiness CG
            if contentgroup == 'SR':

                index+=1

                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree7077")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()

                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        break               
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])

                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")                
                

            ## Download Interventions Beta CG
            elif contentgroup == 'IB':

                index+=1
                
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree7530")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])

                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")

            ## Download Essentilas CG
            elif contentgroup == 'ESS':

                index+=1
                
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree3493")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        time.sleep(2)
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])

                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")

            ## Download Assessment CG
            elif contentgroup == 'AS':
                index+=1                
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree3495")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        time.sleep(2)
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])

                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")

            ## Download RiskAnalysis CG
            elif contentgroup == 'RA':
                index+=1
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree5356")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        time.sleep(2)
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])
                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")   

            ## Download DigitalLearning CG
            elif contentgroup == 'DL':
                index+=1
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree3496")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        time.sleep(2)
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])
                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")                             

            ## Download System And Variables CG
            elif contentgroup == 'SV':
                index+=1
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cstl_MainNavTree3494")))
                element.click()
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_to_click_export))
                )
                element.click()
                
                ## Above click will open a new tab so only new tab should be closed after downlaoding 
                exportwindow = driver.window_handles
                driver.switch_to.window(exportwindow[-1])
                # monitoring the downloading folder if file has been downloaded or not
                while True:
                    allfiles = os.listdir(downloadPath)
                    if len(allfiles)>i:
                        i+=1
                        time.sleep(2)
                        break
                driver.close()
                time.sleep(1)

                ## below code is for next loop so all frames are in place to run download script
                # switching to main window
                driver.switch_to.window(exportwindow[0])
                ## Switch to main/parent frame
                driver.switch_to.default_content()
                ## Again swtich to main/parent frame
                driver.switch_to.default_content()
                ## Switch to new frames one by one
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"migrationsource")))
                driver.switch_to.frame("folderList")
                driver.switch_to.frame("NavTreeFrame")                
            else:
                print("Please give correct CG in input.")
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
    g.reset()
    g.checkout('--','.')
    time.sleep(2)
    g.pull()
    allfiles = os.listdir(downloadPath)
    for x in range(len(allfiles)):
        firstfile = allfiles[x]
        
        # Moving Optional modules into git path
        if firstfile=="InterventionsBeta.7z":
            os.replace(downloadPath + "InterventionsBeta.7z", gitPath + "optional\\InterventionsBeta.7z")
        elif firstfile=="StudentReadiness.7z":
            os.replace(downloadPath + "StudentReadiness.7z", gitPath + "optional\\StudentReadiness.7z")
        elif firstfile=="RiskAnalysis.7z":
            os.replace(downloadPath + "RiskAnalysis.7z", gitPath + "optional\\RiskAnalysis.7z") 

        # Moving Essentials into git path
        elif firstfile=="Essentials.7z":
            os.replace(downloadPath + "Essentials.7z", gitPath + "essentials\\Essentials.7z")

        # Moving Assessments into git path
        elif firstfile=="Assessments.7z":
            os.replace(downloadPath + "Assessments.7z", gitPath + "assessments\\Assessments.7z")

        # Moving DigitalLearning into git path
        elif firstfile=="DigitalLearning.7z":
            os.replace(downloadPath + "DigitalLearning.7z", gitPath + "digital-learning\\DigitalLearning.7z")

         # Moving System And Variables into git path
        elif firstfile=="SystemVariables.7z":
            os.replace(downloadPath + "SystemVariables.7z", gitPath + "essentials\\SystemVariables.7z")

        else:
            
            exit()

#calling functions 




if __name__ == "__main__":

    # ##call function to clear up the path or delete everything
    delete(downloadPath)
    # ## call login functino to download CG
    login(loginLink, "user", myUser, "pass", myPassword, "btnSubmit", cg)
    # ## call rename function to change the file name properly as per requirement
    rename(downloadPath)
    # ## take the pull first and move the file from downloadPath to gitPath
    gitpull(gitPath)