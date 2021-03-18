from sys import exit
import logging
import requests
import pprint
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import re
import time
import pync
from config import Options as op
import utils
import send_email

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(os.getcwd() + '/error.log')

############################################
# Instantiate chrome driver and its options
############################################
kwargs = {}
options = webdriver.ChromeOptions()
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--incognito")
# options.add_argument("--headless")
options.add_argument("--kiosk")
kwargs['options'] = options

driver = webdriver.Chrome(os.getcwd() + "/chromedriver", **kwargs)

############################################
# Constants
NO_AVAILABLE_SITES = 'No Available Sites'

############################################


def notify(URL):
    print('Found one or more sites! Sending you an email now.')

    # Popup notification for MAC users
    if op.OSX == True:
        try:
            pync.notify('One or more sites are available!', title='Sites available!', open=URL)
        except Exception:
            log.error("Could not send notification.")

    #Send email
    if op.NOTIFY_BY_EMAIL:
        send_email.send_email(URL)

def one_true(list_item):
    if (list(map(bool, list_item)).count(True)) == 1:
        return True
    else:
        log.error('One and only one OS should be True in config.')
        return False




def validate_options():
    options = []
    # Only one operating system should be True from the config
    oses = []
    oses.extend([op.OSX, op.WINDOWS, op.LINUX])
    one_os = one_true(oses)
    options.append(one_os)

    # Validate Email
    options.append(utils.valid_email(op.EMAIL))

    # Validate time to retry
    options.append(utils.valid_seconds(op.TIME_TO_RETRY))

    # Validate dates
    options.append(utils.valid_dates(op.START_DATE, op.END_DATE))

    if False in options:
        log.error('Something went wrong. Check config.')
        return False
    else:
        return True


def find_campsites():

    #Get Location IDs if not already present and construct URL
    URL = utils.get_url()

    def check_availability():
        # Load page
        try:
            driver.get(URL)
        except TimeoutException as te:
            log.error(f'Could not load page.\n{te}')

        # Page takes a while to load. Wait until the list view button appears to proceed.
        delay = 3  # seconds
        try:
            list_view = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'list-view-button')))
            print('Done loading')
        except TimeoutException as te:
            print(f'Loading the page is taking too long. \nTimeout Exception: {te}')

        # Enter list view
        list_view = driver.find_element_by_id('list-view-button')
        driver.execute_script("arguments[0].scrollIntoView();", list_view)
        time.sleep(1)
        list_view.click()

        time.sleep(1)

        # Show available sites
        available_sites_checkbox = driver.find_element_by_xpath("//*[@id='mat-checkbox-2-input']")
        if available_sites_checkbox.is_selected():
            pass
        else:
            available_sites_checkbox.click()
        time.sleep(1)

        page_title = driver.find_element_by_id('pageTitle')
        driver.execute_script("arguments[0].scrollIntoView();", page_title)
        time.sleep(1)

        if NO_AVAILABLE_SITES in driver.page_source:
            print(f'There are no sites available for the selected dates. Trying again in {op.TIME_TO_RETRY} seconds.')
            time.sleep(op.TIME_TO_RETRY)
            check_availability()
        else:
            notify(URL)
            # Adding quit here as we only want to stop the process when a campsite is found
            driver.quit()


        # available_sites = driver.find_elements_by_class_name('available')
        # if not available_sites:
        #     print('No available sites')
        #     check_availability()
        # else:
        #     for item in available_sites:
        #         print(item)

    check_availability()



pp = pprint.PrettyPrinter(indent=4)

'''
Begin Process
'''
# Validate Options
validate_options()

# Start Searching
find_campsites()


def login(username, password):
    pass


