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
    def __init__(self, url, user, pwd, comm_type=None, comm_name=None):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.driver = Driver(headless=False, browser_path="./geckodriver").make_driver()
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


    def get_channels_or_dms(self):
        time.sleep(5)
        if self.comm_type == 'channel':
            sidebar_list = self.driver.find_elements_by_xpath('.//span[@class = "p-channel_sidebar__name"]')
            channel_list = []
            for elem in sidebar_list:
                if elem.text not in ['Apps', 'Add a channel']:
                    channel_list.append(elem.text)
                elif elem.text == 'Add a channel':
                    return channel_list


    def select_channel(self, comm_input):
        time.sleep(5)
        # select channel in sidebar
        channel_sidebar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "span[data-qa='channel_sidebar_name_{}']"
                                            .format(comm_input))))

        print("Selecting channel {} /n".format(channel_sidebar.text))
        self.driver.execute_script("arguments[0].click();", channel_sidebar)
        time.sleep(5)

    def select_message(self):
        # up select last message as user
        action1 = ActionChains(self.driver)
        action1.send_keys(Keys.COMMAND).send_keys(Keys.ARROW_UP)
        action1.perform()
        message = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID,
                                                "undefined"
                                                )))
        return message


    def delete_messages(self, comm_list):

        try:
            comm_place = comm_list.index(comm_name)
        except ValueError:
            print("{} {} doesn't exist!".format(comm_type, comm_name))
            raise ValueError

        #get other comms
        comm_before = comm_list[comm_place - 1]
        comm_after = comm_list[comm_place + 1]

        # wait until the side bar is loaded
        time.sleep(5)

        deleted_message_counter = 0

        while deleted_message_counter < 10:
            # select comm to delete from

            retries = 0
            while retries < 10:
                try:
                    self.select_channel(comm_name)
                    message = self.select_message()
                    retries = + 1
                    print(message)
                    if message:
                        retries = 10
                except TimeoutError:
                    print("Deleted {} messages, can't find any more.".format(deleted_message_counter))
                    return None

            message.clear()

            try:
                save_changes_button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "button.c-button:nth-child(2)"
                                                    )))
            except TimeoutError:
                self.close_browser()

            try:
                self.driver.execute_script("arguments[0].click();", save_changes_button)
            except TimeoutError:
                try:
                    self.select_channel(comm_before)
                except ValueError:
                    self.select_channel(comm_after)

                self.select_channel(comm_name)
                message = self.select_message()

            delete_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                ".c-button--danger"
                                                )))

            self.driver.execute_script("arguments[0].click();", delete_button)

            deleted_message_counter += 1
            print("Deleted {} message(s) so far...".format(deleted_message_counter))

            # since text input doesn't seem to be reachable, select other comm to put cursor back in box
            try:
                self.select_channel(comm_before)
            except ValueError:
                self.select_channel(comm_after)

    def close_browser(self):
        self.browser.close()
        time.sleep(3)
        self.browser.quit()


if __name__ == "__main__":
    config = ConfigParser()
    config.read('config/secrets.properties')
    # get inputs
    user = config.get('SlackSection', 'SLACK_GHOST_USER')
    pwd = config.get('SlackSection', 'SLACK_GHOST_PASS')
    workplace = config.get('SlackSection', 'SLACK_GHOST_WORKPLACE')
    comm_type = 'channel'
    comm_name = 'random'

    test_url = 'https://{}.slack.com'.format(workplace)
    slack_ghost = SlackGhost(test_url, user, pwd, comm_type, comm_name)
    slack_ghost.login()
    comm_list = slack_ghost.get_channels_or_dms()
    slack_ghost.delete_messages(comm_list)







