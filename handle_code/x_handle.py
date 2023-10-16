from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import json


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def Login(twitter_username,twitter_password):
    driver.get('https://twitter.com/login')
    element_locator = (By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_field = wait.until(EC.visibility_of_element_located(element_locator))
    username_field.send_keys(twitter_username)
    username_field.send_keys(Keys.ENTER)
    element_locator = (By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_field = wait.until(EC.visibility_of_element_located(element_locator))
    password_field.send_keys(twitter_password)
    check = driver.title
    password_field.send_keys(Keys.ENTER)
    time.sleep(5)
    with open('cookies.txt', 'w') as file:
        json.dump(driver.get_cookies(), file, indent=4)
    if(driver.title != check):
        return True
    return False

def Trends_Location_Selected():
    driver.get('https://twitter.com/i/trends')
    element_locator = (By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/a')
    setting_Location = wait.until(EC.visibility_of_element_located(element_locator))
    setting_Location.click()
    time.sleep(3)
    cb_Location = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/label/div/div[2]/input')
    return cb_Location.is_selected()


def Logout():
    driver.delete_all_cookies()

# if __name__ == "__main__":
    
# #     twitter_username = '@thanh_ngo8742'
# #     twitter_password = '@thanh_ngo8742'
#     #print(Login(twitter_username,twitter_password))
# #     #print(get_Trends())
# #     #print(Get_n_Post_By_Input_Trend("ad",5))
# #     #print(Trends_Location())
#     # while True:
#     #     txt = input("link: ")
#     #     dowload_Video_Or_Photos(txt,"photo","C:\\Users\\Tuan\\Desktop\\x")
#     #get_Text_With_Icon("https://twitter.com/sakamatachloe/status/1713847279374004462")
#     # input()
#     # driver.quit()
    
    