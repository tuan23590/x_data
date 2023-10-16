from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import threading
def dowload(url,name,type):
    response = requests.get(url)
    extend = ""
    if (type=="Video"):
        extend = ".mp4"
    elif (type=="Photo"):
        extend = ".jpg"
    file_name = url_save+'/'+type+'/'+name+extend
    with open(file_name, "wb") as file:
        file.write(response.content)


def dl_handle(List_link,List_name):
    List_Media = []
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    for i in range(0,len(List_link)):
        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("https://savetwitter.net/en/twitter-image-downloader")
        element_locator = (By.XPATH,"//*[@id='s_input']")
        search = wait.until(EC.visibility_of_element_located(element_locator))
        search.send_keys(List_link[i])
        search.send_keys(Keys.ENTER)
        element_locator = (By.XPATH,"//*[@id='search-result']")
        c = 0
        wait.until(EC.visibility_of_element_located(element_locator))
        try:
            div_img = driver.find_element(By.XPATH,"//*[@id='search-result']/div[2]/div/ul")
            url_Photos = div_img.find_elements(By.TAG_NAME, "a")
            for item in url_Photos:
                List_Media.append([item.get_attribute('href'),List_name[i]+'_'+str(c),"Photo"])
                c +=1
        except NoSuchElementException:
            print("No Photo")
        try:
            resus_video = driver.find_elements(By.CSS_SELECTOR, "div.tw-video")
            for item in resus_video:
                url_Video = item.find_element(By.TAG_NAME, "a").get_attribute('href')
                if "Download Photo" in item.find_element(By.TAG_NAME, "a").text:
                    List_Media.append([url_Video,List_name[i]+'_'+str(c),"Photo"])
                    c+=1
                    continue
                List_Media.append([url_Video,List_name[i]+'_'+str(c),"Video"])
                c+=1
        except NoSuchElementException:
            print("No Video")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return List_Media
    
def dowload_Videos_Or_Photos(List_link,List_name,url):
    start_time = time.time()
    global url_save
    url_save = url
    List_Media = dl_handle(List_link,List_name)
    threads = []
    for i in List_Media:
        thread = threading.Thread(target=dowload, args=(i[0],i[1],i[2]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Thời gian thực thi: ", execution_time, "giây")