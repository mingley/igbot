from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

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
        time.sleep(2)
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        time.sleep(2)
        # password_element.send_keys(Keys.RETURN)
        login_button = lambda: self.driver.find_element_by_xpath("//button[@type='submit']")
        login_button().send_keys(Keys.RETURN)
        time.sleep(2)
        
    def get_pictures_on_page(self, hashtag, scrolls=int):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, scrolls):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if
                                 hashtag in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue
        return pic_hrefs


    # write comment in area using a lambda function
    def write_comment(self, comment_text):
        try:
            comment_button = lambda: self.driver.find_element_by_xpath("//span[@aria-label='Comment']")
            comment_button().click()
            time.sleep(1)

        except NoSuchElementException:
            pass
        
        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            time.sleep(1)
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            time.sleep(1)
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1,7)/30))

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False


    def post_comment(self, comment_text):
        time.sleep(random.randint(1,5))

        comment_box_elem = self.write_comment(comment_text)

        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
                post_button().click()
                print('clicked button')
            except NoSuchElementException:
                pass

        time.sleep(random.randint(4,6))
        self.driver.refresh()
        if comment_text in self.driver.page_source:
            return True
        return False
    
    def get_comments(self):

        time.sleep(3)

        # comments = driver.find_elements_by_class_name("C4VMK")

        # comments_list = []

        # for c in comments:
        #     comment = c.find_element_by_css_selector('span').get_attribute("textContent")
        #     user = c.find_element_by_class_name("TlrDj").get_attribute("textContent")
        #     print("" + user + ": " + str(comment))
        #     comments_list.append(comment)

        try:
            comments_in_block = self.driver.find_elements_by_class_name("C4VMK")
            user_comments = [x.find_element_by_css_selector('span').get_attribute('textContent') for x in comments_in_block]

        except NoSuchElementException:
            return ''

        print(user_comments)
        return user_comments


    def comment_on_picture(self):
        bot = ChatBot('Ron Obvious')
        trainer = ListTrainer(bot)
        picture_comment = self.get_comments()
        response = bot.get_response(picture_comment)
        print("users comment", picture_comment)
        print("Bots reply", response)
        return self.post_comment(response)

            


            


        
        
        # pic_hrefs = [href for href in pic_hrefs if '/p/' in href]
        # print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        # for pic_href in pic_hrefs:
        #     driver.get(pic_href)
        #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #     try:
        #         driver.find_element_by_xpath("//span[@aria-label='Like']").click()
        #         time.sleep(18)
        #     except Exception as e:
        #         time.sleep(2)



testIG = InstragramBot(os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD'))
testIG.login()

for pic in testIG.get_pictures_on_page(hashtag='crossfit', scrolls=5)[1:]:
    testIG.driver.get(pic)
    time.sleep(3)
    print('Posted Comment:', testIG.comment_on_picture())
    time.sleep(3)

    # def like_photo(self, hashtag):
    #     driver = self.driver
    #     driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
    #     time.sleep(2)
    #     for i in range(1,3):
    #         driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    #         time.sleep(2)

    #     #searching for pic link
    #     hrefs = driver.find_elements_by_tag_name('a')
    #     pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
    #     pic_hrefs = [href for href in pic_hrefs if '/p/' in href]
    #     print(hashtag + ' photos: ' + str(len(pic_hrefs)))

    #     for pic_href in pic_hrefs:
    #         driver.get(pic_href)
    #         driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    #         try:
    #             driver.find_element_by_xpath("//span[@aria-label='Like']").click()
    #             time.sleep(18)
    #         except Exception as e:
    #             time.sleep(2)