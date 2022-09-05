import requests
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from base_scraper import ScrapperSelenium
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from pictures import Media

sleep_instagram = lambda t: np.random.randint(low=t / 2, high=t * 2, size=1)

link = 'https://www.instagram.com/'


class InstagramScraper(ScrapperSelenium):
    def __init__(self, username, password, require_login=True):
        super().__init__()
        self.driver.get(link)
        self.content = []
        sleep((sleep_instagram(4))[0])
        login = not require_login
        self.pics = []
        # login to account:
        if require_login:
            while not login:
                try:
                    self.fetch_element(By.NAME, 'username').send_keys(username)
                    self.fetch_element(By.NAME, 'password').send_keys(password)
                    self.fetch_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
                    sleep((sleep_instagram(4))[0])
                    # skip save information
                    self.fetch_element(By.XPATH,
                                       '//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
                    sleep((sleep_instagram(4))[0])
                    login = True

                except:
                    self.fetch_element(By.NAME, 'username').clear().send_keys(username)
                    self.fetch_element(By.NAME, 'password').clear().send_keys(password)

    def fetch_everything(self, account):
        # search user:
        # txt_field = self.fetch_element(By.XPATH, '//*[@id="mount_0_0_M8"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input')
        # txt_field.send_keys(account).perform()
        self.driver.get(f'{link}/{account}/')
        sleep((sleep_instagram(4))[0])
        self.scrape_down()
        all_media = self.get_rows()
        page_content = pd.DataFrame(columns=['index', 'caption', 'time', 'tags'])
        for i, media in enumerate(all_media):
            media.click()
            caption, time, tags = self.pictures_details(i)
            self.load_comments(i)
            all_media.append({'index': i, 'caption': caption, 'time': time, 'tags': tags})
            self.fetch_element(By.XPATH,
                               '//div[@class="om3e55n1 b6ax4al1"]/*[name()="svg"][@aria-label="Close"]').click()
        page_content.to_csv(f'{account}.csv')

    def update_media(self, id, **kwargs):
        for m in self.content:
            if m == id:
                return "skip"
        # m = Media(id, kwargs)
        return "New"

    def check_elements(self, elements):
        for e in elements:
            if 'New' == self.update_media(e.id):
                # only scrape the rows to add pictures
                self.content.append(e.id)
                self.extract_content(e)

    def extract_content(self, element):
        pics = element.find_elements_by_css_selector(r'div._aabd._aa8k._aanf')
        for p in pics:
            pic = p.click()
            e = Media(p.id, details)
            self.content.append(e)

    def scrape_down(self):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            potential_elements = self.get_rows()
            self.check_elements(potential_elements)
            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                print("END OF PAGE")
            last_height = new_height

    def get_rows(self, class_name1='_ac7v', class_name2='_aang'):
        res = self.driver.find_elements(By.CSS_SELECTOR, r'div._ac7v._aang')
        return res

    def pictures_details(self,el, id):
        caption = el.find_element_by_css_selector()
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


insta_bot = InstagramScraper('baztabhonarai', 'fatemesara1401', True)
insta_bot.fetch_everything('alisdrinks')
