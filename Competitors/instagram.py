import requests
from abc import ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from base_scraper import ScrapperSelenium
from selenium.webdriver.common.by import By

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

    def fetch_everything(self, account, db_name=None):
        # search user:
        self.fetch_element(By.XPATH, 'https://python-patterns.guide/').send_keys(account)

    def pictures_loading(self):

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


