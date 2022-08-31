import requests
from abc import ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class ScrapperSelenium:

    def __init__(self):
        driver_path = 'C:\AI-team-development\chromedriver'
        self.DRIVER_PATH = driver_path
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.DRIVER_PATH)
        self.driver.delete_all_cookies()
        self.wait = WebDriverWait(self.driver, 30)
        action = ActionChains(self.driver)

    @staticmethod
    def parse_element_tag(web_element, tag):
        assert tag is not None, 'tag must be specified to be searched in the html content'
        parser = BeautifulSoup(web_element, 'html.parser')
        return parser.find_all(tag)

    def fetch_element(self, by, string):
        res = self.wait.until(EC.visibility_of_element_located((by, string)))
        return res

