import requests
import urllib

from abc import ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from base_scraper import ScrapperSelenium
from selenium.webdriver.common.by import By
import pandas as pd

sleep_instagram = 5


class InstagramScraper(ScrapperSelenium):
    def __int__(self, username, password, require_login=False):
        super(InstagramScraper, self).__init__()
        self.driver.get('https://www.instagram.com/')
        sleep(sleep_instagram)
        # login to account:
        if require_login:
            self.fetch_element(By.NAME, 'username').send_keys(username)
            self.fetch_element(By.NAME, 'password').send_keys(password)
            self.driver.find_element_by_css_selector(
                '#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child() > button').click()
            sleep(sleep_instagram)
            # skip save information
            self.driver.find_element_by_css_selector(
                'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
            sleep(sleep_instagram)

    def fetch_everything(self, account):
        # search user:
        self.fetch_element(By.XPATH, '//*[@id="mount_0_0_Oh"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/div[1]/div').send_keys(account)
        self.scroll_down()
        all_media = self.get_pictures()
        page_content = pd.DataFrame(columns=['index', 'caption', 'time', 'tags'])
        for i, media in enumerate(all_media):
            media.click()
            caption, time, tags = self.pictures_details(i)
            self.load_comments(i)
            all_media.append({'index': i, 'caption': caption, 'time': time, 'tags': tags})
            self.fetch_element(By.XPATH, '//div[@class="om3e55n1 b6ax4al1"]/*[name()="svg"][@aria-label="Close"]').click()
        page_content.to_csv(f'{account}.csv')

    def scroll_down(self):

        scroll_pause_time = 2
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_pictures(self, class_name='_aagw'):
        res = self.fetch_element(By.CLASS_NAME, class_name)
        return res

    def pictures_details(self, id):
        caption = self.fetch_element(By.CLASS_NAME, '_a9zs')
        time = self.fetch_element(By.XPATH,
                                  '//*[@id="mount_0_0_lJ"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time').get_attribute(
            "datetime")
        tags = []
        image_url = self.fetch_element(By.XPATH,
                                       '//*[@id="mount_0_0_lJ"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div/div[1]/img').get_attribute(
            'src')
        video_url = self.fetch_element(By.XPATH,
                                       '//*[@id="mount_0_0_Os"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div[1]/div/div/video').get_attribute(
            'src'
        )
        link = image_url if image_url is not None else video_url

        urllib.urlretrieve(link, f"{id}.png")

        return caption, time, tags

    def load_comments(self, id):
        df = pd.DataFrame(columns=['id, time, comment'])
        more_comments = self.fetch_element(By.CLASS_NAME, '_ab6-')
        while more_comments is not None:
            more_comments.click()
            more_comments = self.fetch_element(By.CLASS_NAME, '_ab6-')
        all_comments = self.fetch_element(By.CLASS_NAME, '_a9zr')
        for comment in all_comments:
            date = comment.get_attribute("datetime")
            account_name = comment.get_attribute("a").text
            comment = comment.get_attribute("a").text
            comment_details = {}
            all_comments.append(comment_details, ignore_index=True)
        all_comments.to_csv(f'{id}.csv')
