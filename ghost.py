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

# use an automated testing driver
def make_driver():
    moz_driver = "./geckodriver"

    # headless mode
    # options = Options()
    # options.add_argument('-headless')
    # driver = webdriver.Firefox(executable_path=moz_driver, firefox_options=options)

    # browser visible mode
    driver = webdriver.Firefox(executable_path=moz_driver)
    return driver


# Login into slack
def login_account(driver, url, username, password):
    driver.get(url)
    send_keys(username + Keys.TAB + password + Keys.TAB)
    time.sleep(5)

if __name__ == "__main__":
    config = ConfigParser()
    config.read('config/secrets.properties')
    username = config.get('SlackSection', 'SLACK_GHOST_USER')
    password = config.get('SlackSection', 'SLACK_GHOST_PASS')

    url = 'https://testingghost.slack.com'
    driver = make_driver()
    login_account(driver, url, username, password)





