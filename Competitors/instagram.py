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
        # all_media = self.get_rows()
        # page_content = pd.DataFrame(columns=['index', 'caption', 'time', 'tags'])
        # for i, media in enumerate(all_media):
        #     media.click()
        #     caption, time, tags = self.pictures_details(i)
        #     self.load_comments(i)
        #     all_media.append({'index': i, 'caption': caption, 'time': time, 'tags': tags})
        #     self.fetch_element(By.XPATH,
        #                        '//div[@class="om3e55n1 b6ax4al1"]/*[name()="svg"][@aria-label="Close"]').click()
        # page_content.to_csv(f'{account}.csv')

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

    def update_media(self, id):
        for m in self.content:
            if m == id:
                return "skip"
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
            p.click()
            sleep_instagram(10)
            image_url = self.driver.find_element_by_css_selector('img._aagt').get_attribute("src")
            url = self.driver.current_url.replace('https://www.instagram.com/', '')
            sleep_instagram(6)
            like_view = self.driver.find_element_by_css_selector('section._ae5m._ae5n._ae5o').text
            if 'likes' in like_view:
                like_view = like_view.replace(' likes', '')
                type_media = 0
            else:
                like_view = like_view.replace(' views', '')
                type_media = 1
            sleep_instagram(3)
            comments = self.driver.find_element_by_css_selector('ul._a9z6._a9za')
            details = self.scrape_down_comments(comments)
            e = Media(url, image_url, type_media, details, like_view)
            self.content.append(e)
            self.driver.execute_script("window.history.go(-1)")
            sleep_instagram(8)

    def scrape_down_comments(self, comment_blocks):
        more_btn = comment_blocks.find_element_by_css_selector("svg._ab6-")
        btn_empty = lambda location: True if location['x'] != 0 else False
        while btn_empty(more_btn.location):
            self.click_on_element(more_btn)
        list_of_comments = comment_blocks.find_elements_by_css_selector("div._a9zo")
        comments_dict = []
        for c in list_of_comments:
            user_id = c.find_element_by_css_selector(
                "a.qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h"
                ".l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq"
                "._acan._acao._acat._acaw._a6hd").text,
            comment = c.find_element_by_css_selector("span._aacl._aaco._aacu._aacx._aad7._aade").text
            dt = c.find_element_by_css_selector("time._a9ze._a9zf").get_attribute("datetime")
            comments_dict.append([user_id, comment, dt])
        return comments_dict


    def get_rows(self, class_name1='_ac7v', class_name2='_aang'):
        res = self.driver.find_elements(By.CSS_SELECTOR, r'div._ac7v._aang')
        return res

    def pictures_details(self, el, id):
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

    def publish_data(self,file_name):
        pic_detail = pd.DataFrame(columns=['pic_id', 'pic_url', 'number_of_comments', 'like/view', 'caption', 'date'])
        comment_detail = pd.DataFrame(columns=['pic_id', 'user', ''])
        for pic in self.contnt:
            media = pic.pic_into_txt()
            comments = pic.comment_to_txt()
            pic_detail.append(media)
            comment_detail.append(comments)
        pic_detail.to_csv(f'{file_name}_pics.csv')
        comment_detail.to_csv(f'{file_name}_comment.csv')


insta_bot = InstagramScraper('baztabhonarai', 'fatemesara1401', True)
insta_bot.fetch_everything('alisdrinks')
