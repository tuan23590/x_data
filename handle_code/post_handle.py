from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import json

def get_Text_With_Icon(link,driver):
    wait = WebDriverWait(driver, 10)
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)
    element_locator =(By.XPATH,"//div[@data-testid='tweetText']")
    txt = wait.until(EC.visibility_of_element_located(element_locator))
    child_elements = txt.find_elements(By.XPATH,".//*")
    result_string = ""
    for element in child_elements:
        if element.tag_name == "span":
            text = element.text
            result_string += text + " "
        elif element.tag_name == "img":
            alt_value = element.get_attribute("alt")
            result_string += alt_value + " "   
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result_string


def Get_n_Post_By_Input_Trend(trend,n):
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
        List_Post = []
        trend_rep = trend.replace('@', '').replace('#', '').replace('%', '')
        driver.get('https://twitter.com/search?q='+trend_rep+'&src=trend_click&vertical=trends')
        count = 0 
        time.sleep(5)
        per_link = ""
        scroll = 0
        while (count<n):
            driver.execute_script('window.scrollTo(0, '+str(scroll)+')')
            scroll+=500
            time.sleep(1)
            div_Post = driver.find_element(By.CLASS_NAME, "r-kzbkwu")
            link = div_Post.find_elements(By.TAG_NAME, "a")[2].get_property('href')
            if "twitter.com" in link and "status" in link:
                now_link= link
            if(now_link!=per_link):
                print(link)
                count +=1
                per_link = now_link
                link = div_Post.find_elements(By.TAG_NAME, "a")[2].get_property('href')
                div_Name = div_Post.find_element(By.XPATH,"//div[@data-testid='User-Name']").find_elements(By.TAG_NAME,"a")[0].text
                div_Username = div_Post.find_element(By.XPATH,"//div[@data-testid='User-Name']").find_elements(By.TAG_NAME,"a")[1].text
                status = get_Text_With_Icon(link,driver)
                share = div_Post.find_elements(By.CSS_SELECTOR,"div.r-adacv") 
                tags = re.findall(r'[#@]\w+', status)
                tags = list(set(tags))
                div_interactions = div_Post.find_element(By.CSS_SELECTOR,"div.r-1ye8kvj")
                interactions = div_interactions.find_elements(By.CSS_SELECTOR,"div.r-13awgt0")
                print("--------------------------------------")
                List_Post_Data = []
                List_Post_Data.append(link)
                List_Post_Data.append(div_Name)
                List_Post_Data.append(div_Username)
                List_Post_Data.append(status)
                List_Post_Data.append(tags)
                List_Post_Data.append(interactions[0].text)
                List_Post_Data.append(interactions[1].text)
                List_Post_Data.append(interactions[2].text)
                List_Post_Data.append(interactions[3].text)
                List_Post_Data.append(trend)
                List_Post.append(List_Post_Data)
                #print("Name: "+div_Name)
                #print("User: "+div_Username)
                # print("Status: "+status)
                # print("Tag:",*tags)
                # print("Reply: "+interactions[0].text)
                # print("Repost: "+interactions[1].text)
                # print("Like: "+interactions[2].text)
                # print("View: "+interactions[3].text)
                # dowload_Video_Or_Photos(link,div_name[1].text)
                print("--------------------------------------")
        driver.quit()
        return List_Post
    driver.quit()
    