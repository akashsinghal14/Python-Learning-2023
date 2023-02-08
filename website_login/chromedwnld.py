from selenium import webdriver
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # to add wait time while browser loading or downloading 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import sys # to ask for cmd line arguments when executing




chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("download.default_directory=C:\\Users\\singhala\\Documents\\Leraning 2023\\PythonCode\\website_login\\")


chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "C:\\Users\\singhala\\Documents\\Leraning 2023\\PythonCode\\website_login\\"
})
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://chromedriver.storage.googleapis.com/index.html?path=110.0.5481.30/")
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/table/tbody/tr[4]/td[2]/a").click()
time.sleep(5)

