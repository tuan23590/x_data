from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
def get_Trends():
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
        driver.get('https://twitter.com/i/trends')
        
        element_locator = (By.XPATH,"//div[@aria-label='Timeline: Trends']")
        list_t = wait.until(EC.visibility_of_element_located(element_locator))

        driver.execute_script('window.scrollTo(0,1000 )')
        time.sleep(2)
        list_trend = driver.find_elements(By.XPATH,"//div[@class='css-1dbjc4n r-16y2uox r-bnwqim']")
        print(len(list_trend))
        List = []
        for i in list_trend:
            trend = i.find_elements(By.CSS_SELECTOR, "div[dir='ltr'], div[dir='rtl']")
            for j in trend:
                print(j.text)
            # print("Name Of Trend: "+trend[3].text)
            # print("Count Post: "+trend[4].text)
            #print("----------------------------------------------")
            Li = [trend[3].text,trend[4].text]
            List.append(Li)
        return List
    driver.quit()
    return False