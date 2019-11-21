#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# waits
import time

# properties
from configparser import ConfigParser


class Driver(object):
    """ Driver Instantiates an automated testing driver
        headless: see the browser for development
        browser_path: path to actual executable. Download here - https://www.seleniumhq.org/download/
    """
    def __init__(self, headless=False, browser_path = "./geckodriver"):
        self.headless = headless
        self.browser_path = browser_path

    def make_driver(self):
            # headless mode
        if self.headless == True:
            options = Options()
            options.add_argument('-headless')
            driver = webdriver.Firefox(executable_path=self.browser_path, firefox_options=options)
        else:
            # browser visible mode
            driver = webdriver.Firefox(executable_path=self.browser_path)

        return driver


class SlackGhost(Driver):
    def __init__(self, url, user, pwd, comm_type=None, comm_name=None):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.driver = Driver().make_driver()
        self.comm_type = comm_type
        self.comm_name = comm_name

    def login(self):

        self.driver.get(self.url)

        # fill out user & password
        self.driver.find_element_by_id("email").send_keys(self.user)
        self.driver.find_element_by_id("password").send_keys(self.pwd)

        # uncheck remember me button
        self.driver.execute_script("document.getElementsByClassName"
                              "('checkbox normal inline_block small_right_margin')[0].click()")

        # sign in
        self.driver.execute_script("document.getElementById('signin_btn').click()")


    def delete_messages(self):
        # wait until the side bar is loaded
        time.sleep(5)
        #if self.comm_type == 'channel':

        # select channel in sidebar
        channel_sidebar = self.driver.find_elements_by_css_selector("span[data-qa='channel_sidebar_name_{}']".format(self.comm_name))
        self.driver.execute_script("arguments[0].click();", channel_sidebar[0])

        # select messages
        time.sleep(5)
        print("select messages")
        messages = self.driver.find_elements_by_class_name('c-message__body')
        print(messages[1])

        #for message in messages

        ActionChains(self.driver).move_to_element(messages[1]).perform()
        messages[1].click()

        print("opening the dropdown")
        time.sleep(5)
        print("deleting")

        self.driver.switch_to.frame(frame)
        dropdown = self.driver.find_element_by_css_selector("body > div.ReactModalPortal")

        print(dropdown)
        self.driver.execute_script("arguments[0].click();", dropdown)

        print(delete_drop)
        time.sleep(5)
        delete_drop = self.driver.find_elements_by_css_selector("span[data-qa='delete_message']")
        delete_drop.click()

        #for message in delete_drop:
            #self.driver.execute_script("arguments[0].click();", message)



if __name__ == "__main__":
    config = ConfigParser()
    config.read('config/secrets.properties')
    user = config.get('SlackSection', 'SLACK_GHOST_USER')
    pwd = config.get('SlackSection', 'SLACK_GHOST_PASS')

    test_url = 'https://testingghost.slack.com'

    comm_type = 'channel'

    comm_name = 'random'

    slack_ghost = SlackGhost(test_url, user, pwd, comm_type, comm_name)
    slack_ghost.login()
    slack_ghost.delete_messages()







