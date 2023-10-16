from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
from selenium.common.exceptions import TimeoutException
import time
import re
import urllib.request
import requests
import os
import json
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.maximize_window()
def Login_with_cookies():
    driver.get('https://twitter.com/login')
    element_locator = (By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    wait.until(EC.visibility_of_element_located(element_locator))
    check = driver.title
    if os.path.exists("cookies.txt"):
        with open('cookies.txt', 'r') as file:
            data = json.load(file)
        for item in data:
            driver.add_cookie(item)
        driver.get('https://twitter.com/')
        time.sleep(2)
    if(driver.title != check):
        return True
    return False
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
def Get_Trends():
    driver.get('https://twitter.com/i/trends')
    element_locator = (By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div')
    div_Trends = wait.until(EC.visibility_of_element_located(element_locator))
    list_Trends = div_Trends.find_elements(By.CLASS_NAME, "r-16y2uox")
    for item in list_Trends:
        print(item.find_element(By.CLASS_NAME, "r-1bymd8e").text)
def dowload_Video_Or_Photos(link,name,url):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://savetwitter.net/en/twitter-image-downloader")
    search = driver.find_element(By.XPATH,"//*[@id='s_input']")
    search.send_keys(link)
    search.send_keys(Keys.ENTER)
    try:
        element_locator = (By.XPATH,"//*[@id='search-result']/div[2]/div/ul")
        div_img = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(element_locator))
        url_Photos = div_img.find_elements(By.TAG_NAME, "a")
        c = 0
        for item in url_Photos:
            response = requests.get(item.get_attribute('href'))
            file_name = url+'/Photo/'+name+str(c)+'.jpg'
            with open(file_name, "wb") as photo_file:
                photo_file.write(response.content)
            c +=1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except TimeoutException:
        None
    try:
        element_locator = (By.XPATH,"//*[@id='search-result']")
        div_video = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(element_locator))
        element_locator = driver.find_elements(By.CSS_SELECTOR, "div.tw-video")
        c =0
        for item in element_locator:
            url_Video = item.find_element(By.TAG_NAME, "a").get_attribute('href')
            if "Download Photo" in item.find_element(By.TAG_NAME, "a").text:
                response = requests.get(url_Video)
                file_name = url+'/Photo/'+name+str(c)+'.jpg'
                with open(file_name, "wb") as video_file:
                    video_file.write(response.content)
                c+=1
                continue
            response = requests.get(url_Video)
            file_name = url+'/Video/'+name+str(c)+'.mp4'
            with open(file_name, "wb") as video_file:
                video_file.write(response.content)
            c+=1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except TimeoutException:
        None
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return False
def get_Text_From_Viewmore(link):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)
    element_locator =(By.XPATH,"//div[@data-testid='tweetText']")
    txt = wait.until(EC.visibility_of_element_located(element_locator))
    txt = txt.text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return txt
def Get_n_Post_By_Input_Trend(trend,n):
    List_Post = []
    driver.get('https://twitter.com/search?q='+trend+'&src=typed_query&f=top')
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
            status = get_Text_From_Viewmore(link)
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
    return List_Post
def Trends_Location_Selected():
    driver.get('https://twitter.com/i/trends')
    element_locator = (By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/a')
    setting_Location = wait.until(EC.visibility_of_element_located(element_locator))
    setting_Location.click()
    time.sleep(3)
    cb_Location = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/label/div/div[2]/input')
    return cb_Location.is_selected()
def get_Trends():
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
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
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return List
def change_location():
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://twitter.com/settings/trends/location")
    while True:
        time.sleep(1)
        if driver.current_url != "https://twitter.com/settings/trends/location":
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return
def Logout():
    driver.delete_all_cookies()
if __name__ == "__main__":
    twitter_username = '@thanh_ngo8742'
    twitter_password = '@thanh_ngo8742'
    #print(Login(twitter_username,twitter_password))
    #print(get_Trends())
    #print(Get_n_Post_By_Input_Trend("ad",5))
    #print(Trends_Location())
    dowload_Video_Or_Photos("https://twitter.com/vminnightsky/status/1713617236278038697","photo","C:\\Users\\Tuan\\Desktop\\x")
    #print(get_Text_From_Viewmore("https://twitter.com/wideawake_media/status/1710976951316283488"))
    input()
    driver.quit()
    