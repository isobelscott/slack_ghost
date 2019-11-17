#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

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

        self.driver.execute_script("document.getElementsByClassName"
                                   "('c-button-unstyled p-channel_sidebar__section_heading_label p-channel_sidebar__section_heading_label--clickable')[0].click()")


        # search channels or messages
        time.sleep(5)
        actions = ActionChains(self.driver)
        actions.send_keys(self.comm_name).send_keys(Keys.TAB)
        actions.perform()
        # select the first item returned
        time.sleep(5)
        self.driver.execute_script("document.getElementsByClassName"
                                   "('p-channel_browser_list_item')[0].click()")

        # delete messages
        time.sleep(5)
        print("Finding message...")

        #elem = "/html/body/div[2]/div/div/div[4]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[25]/div/div[3]/span"

        elems = self.driver.find_elements_by_css_selector("span[data-qa='message-text']")

        self.driver.execute_script("arguments[0].click();", elems[1])

        print("clicking dropdown...")
        self.driver.execute_script("document.getElementsByClassName"
                                   "('ReactModal__Body - -open').click()")

        print("Deleting message...")
        self.driver.execute_script("document.getElementsByClassName"
                                   "('c-button-unstyled p-message_actions_menu__delete_message c-menu_item__button c-menu_item__button--danger')[0].click()")





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







