from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random
import re
import dotenv
import os

dotenv.load_dotenv()

class InstragramBot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        # time.sleep(2)
        # login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=']") 
        # login_button.click() 
        time.sleep(2)
        user_name_element = driver.find_element_by_xpath("//input[@name='username']") 
        user_name_element.clear() #clears/deletes anything in the input field
        user_name_element.send_keys(self.username)
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(3)
        
    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        for i in range(1,3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)

        #searching for pic link
        hrefs = driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        pic_hrefs = [href for href in pic_hrefs if '/p/' in href]
        print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                time.sleep(18)
            except Exception as e:
                time.sleep(2)


testIG = InstragramBot(os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'))
testIG.login()
testIG.like_photo("fitness")

hashtags = ['crossfit', 'fitnessmotivation','miramar']