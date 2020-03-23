#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# waits
import time

# properties
from configparser import ConfigParser


class Driver(object):
    """ Driver Instantiates an automated testing driver
        headless: see the browser for development
        browser_path: path to actual executable. Download here - https://www.seleniumhq.org/download/
    """
    def __init__(self, headless, browser_path):
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


class SlackGhost(object):
    """The SlackGhost gets a driver from Driver and can log into account as user and delete messages
    """
    def __init__(self, url, user, pwd, headless, comm_type, comm_name, number_messages_to_delete):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.driver = Driver(headless=headless, browser_path="./geckodriver").make_driver()
        self.comm_type = comm_type
        self.comm_name = comm_name
        self.number_messages_to_delete = number_messages_to_delete

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



    def select_channel(self, select_comm):

        time.sleep(5)
        if self.comm_type == 'channel':
            # select channel in sidebar
            channel_sidebar = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "span[data-qa='channel_sidebar_name_{}']"
                                                .format(select_comm))))

            print("Selecting channel {} \n".format(channel_sidebar.text))
            self.driver.execute_script("arguments[0].click();", channel_sidebar)
            time.sleep(5)

        else:
            # select user chat in sidebar
            print("Go to user")
            time.sleep(5)

            self.driver.execute_script("document.getElementsByClassName"
                                       "('c-button-unstyled p-channel_sidebar__section_heading_label p-channel_sidebar__section_heading_label--clickable')[1].click()")

            time.sleep(5)
            self.driver.find_element_by_id('dm-browser').send_keys(select_comm)

            time.sleep(5)
            self.driver.execute_script("document.getElementsByClassName"
                                       "('c-unified_member__entity-text-container')[0].click()")


    def select_message(self):

        time.sleep(5)

        self.driver.execute_script("document.getElementsByClassName"
                                       "('ql-editor ql-blank')[0].click()")

        action = ActionChains(self.driver)
        action.send_keys("Erasing commenced....")

        time.sleep(5)
        # up select last message as user
        action = ActionChains(self.driver)
        action.send_keys(Keys.COMMAND).send_keys(Keys.ARROW_UP)
        action.perform()
        time.sleep(5)
        message = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID,
                                                    "undefined"
                                                    )))
        if not len(message.text) == 0:
            #try again
            action.send_keys(Keys.COMMAND).send_keys(Keys.ARROW_UP)
            action.perform()
            message = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID,
                                                "undefined"
                                                )))

        return message


    def delete_messages(self, comm_list=None):

        self.select_channel(self.comm_name)
        # wait until the side bar is loaded
        time.sleep(5)
        deleted = 0

        while deleted < self.number_messages_to_delete:
                message = self.select_message()

                if len(message.text) == 0:
                    # wait a bit and try again
                    print("Trying again to get message")
                    time.sleep(5)
                    message = self.select_message()

                if len(message.text) > 0:
                    message.clear()
                    save_changes_button = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR,
                                                            "button.c-button:nth-child(2)"
                                                            )))

                    self.driver.execute_script("arguments[0].click();", save_changes_button)

                    delete_button = WebDriverWait(self.driver, 20).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                            ".c-button--danger"
                                                            )))

                    self.driver.execute_script("arguments[0].click();", delete_button)

                    deleted += 1
                    print("Deleted {} message(s) so far...".format(deleted))

                else:
                    break

        print("Deleted {} messages. All done.".format(deleted))
        self.close_driver()


    def close_driver(self):
        self.driver.close()
        print("Closing driver...")
        time.sleep(3)
        self.driver.quit()
        print("Quiting driver...")



if __name__ == "__main__":
    config = ConfigParser()
    config.read('config/secrets.properties')
    # get inputs
    credential_section = 'SlackSection'
    user = config.get(credential_section, 'SLACK_GHOST_USER')
    pwd = config.get(credential_section, 'SLACK_GHOST_PASS')
    workplace = config.get(credential_section, 'SLACK_GHOST_WORKPLACE')

    # User imputs
    #comm_type = 'channel'
    #comm_name = 'general'
    comm_type = 'messages'
    comm_name = 'Slackbot'

    number_of_messages_to_delete = 20


    test_url = 'https://{}.slack.com'.format(workplace)
    headless = True
    slack_ghost = SlackGhost(test_url, user, pwd, headless, comm_type, comm_name, number_of_messages_to_delete)
    slack_ghost.login()
    slack_ghost.delete_messages()







