from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
def change_location():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get('https://twitter.com/login')
    element_locator = (By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    wait.until(EC.visibility_of_element_located(element_locator))
    check = driver.title
    if os.path.exists("cookies.txt"):
        with open('cookies.txt', 'r') as file:
            data = json.load(file)
        for item in data:
            driver.add_cookie(item)
        driver.get('https://twitter.com/login')
        time.sleep(2)
    if(driver.title != check):
        driver.get("https://twitter.com/settings/trends/location")
        while True:
            time.sleep(1)
            if driver.current_url != "https://twitter.com/settings/trends/location":
                driver.quit()
                return True
    driver.quit()
    return False
    

