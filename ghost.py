#!/usr/bin/env python

import requests
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
            browser = webdriver.Firefox(executable_path=self.browser_path, firefox_options=options)
        else:
            # browser visible mode
            browser = webdriver.Firefox(executable_path=self.browser_path)

        return browser


class SlackGhost(Driver):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.pwd = pwd

    def login(self):
        driver = Driver().make_driver()
        driver.get(self.url)

        username = driver.find_element_by_id("email")
        username.send_keys(user)

        password = driver.find_element_by_id("password")
        password.send_keys(pwd)

        #uncheck remember me button
        driver.execute_script("document.getElementsByClassName"
                              "('checkbox normal inline_block small_right_margin')[0].click()")

        #signin
        driver.execute_script("document.getElementById('signin_btn').click()")


if __name__ == "__main__":
    config = ConfigParser()
    config.read('config/secrets.properties')
    user = config.get('SlackSection', 'SLACK_GHOST_USER')
    pwd = config.get('SlackSection', 'SLACK_GHOST_PASS')

    test_url = 'https://testingghost.slack.com'

    SlackGhost(test_url, user, pwd).login()







