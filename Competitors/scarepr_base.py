import requests
from abc import ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


class ScrapperSelenium:

    def __init__(self, driver_path='/usr/bin/chromedriver'):

        self.DRIVER_PATH = driver_path
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.DRIVER_PATH)

    @staticmethod
    def parse_element_tag(web_element, tag):
        assert tag is not None, 'tag must be specified to be searched in the html content'
        parser = BeautifulSoup(web_element, 'html.parser')
        return parser.find_all(tag)

    def fetch_element(self, by, string):
        res = None
        while res is None:
            try:
                res = self.driver.find_element(by, string)
            except NameError:
                time.sleep(0.2)
                print(' ... loading ... ')
        return res
