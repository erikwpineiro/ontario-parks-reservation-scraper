import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import re
from urllib import parse
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException
from config import Options as op
import datetime


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(os.getcwd() + '/error.log')

kwargs = {}
options = webdriver.ChromeOptions()
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--incognito")
# options.add_argument("--headless")
options.add_argument("--kiosk")
kwargs['options'] = options

park_driver = webdriver.Chrome(os.getcwd() + "/chromedriver", **kwargs)

def wait(by):
    delay = 3
    try:
        list_view = WebDriverWait(park_driver, delay).until(by)
    except TimeoutException as te:
        print(f'Loading the page is taking too long. \nTimeout Exception: {te}')


def get_location(park, campground):

    try:
        park_driver.get('https://reservations.ontarioparks.com/')
    except TimeoutException as te:
        print(f'Could not load Ontario Parks website. \n{te}')

    # Wait for page to load
    wait(EC.presence_of_element_located((By.XPATH, './/*[@formcontrolname="park"]')))

    try:
        park_driver.find_element_by_xpath('.//*[@formcontrolname="park"]').click()
        time.sleep(2)

        park_driver.find_element_by_xpath(f'.//span[@class="mat-option-text" and contains(text(), "{park}")]').click()

        equipment = park_driver.find_element_by_xpath('.//*[@formcontrolname="equipment"]')
        time.sleep(1)
        equipment.find_element_by_xpath('.//ancestor::div[@class="mat-form-field-wrapper"]').click()

        park_driver.find_element_by_xpath(f'.//span[@class="mat-option-text" and contains(text(), "Single Tent")]').click()

        park_driver.find_element_by_class_name('btn-update-search').click()

        wait(EC.presence_of_element_located((By.ID, 'list-view-button')))

        # campground_dot = park_driver.find_element_by_xpath(f'.//*[@id="{campground}"]')
        # campground_dot.find_element_by_xpath('.//ancestor::div[@class="leaflet-marker-icon"]').click()

        wait(EC.presence_of_element_located((By.ID, 'list-view-button')))

        # Enter list view
        park_driver.find_element_by_id('list-view-button').click()
        time.sleep(2)

        # Show available sites
        park_driver.find_element_by_xpath('//div[contains(text(), "Show available")]').click()

        time.sleep(2)

        campground_title = park_driver.find_element_by_xpath(f'.//h3[contains(text(), "{campground}")]')
        park_driver.execute_script("arguments[0].scrollIntoView();", campground_title)
        campground_title.find_element_by_xpath('.//ancestor::div[1]').click()
        time.sleep(5)

    except NoSuchElementException as nsee:
        print(f'Could not find the requested element.\n{nsee}')

    except StaleElementReferenceException as see:
        print(f'Element loaded but was not available at time of action.\n{see}')

    except ElementNotVisibleException as enve:
        print(f'Element is not visible. It may be behind another element.\n{enve}')

    except ElementClickInterceptedException as ecie:
        print(f'Another element is in the way of clicking the desired element.\n{ecie}')

    except ElementNotInteractableException as enie:
        print(f'Could not interact with the element. i.e. perhaps it is a label.\n{enie}')

    except Exception as e:
        print(f'Something went wrong.\n{e}')


    landed_url = park_driver.current_url

    url_dict = dict(parse.parse_qs(parse.urlsplit(landed_url).query))

    park_driver.quit()

    return url_dict


def get_url():
    now = datetime.datetime.now()
    url_components = get_location(op.LOCATION, op.CAMPGROUND)
    location_id = url_components['resourceLocationId'][0]
    campground_id = url_components['mapId'][0]
    URL = f'https://reservations.ontarioparks.com/create-booking/results?resourceLocationId={location_id}&mapId={campground_id}&searchTabGroupId=0&bookingCategoryId=0&startDate={op.START_DATE}&endDate={op.END_DATE}&nights={op.NUMBER_OF_NIGHTS}&isReserving=true&equipmentId=-32768&subEquipmentId=-32768&partySize=1&searchTime={now}'
    return URL


def valid_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if op.NOTIFY_BY_EMAIL == False:
        return True
    elif (re.search(regex, email)):
        return True
    else:
        log.error('Incorrect format for email address used in config.')
        return False



def valid_seconds(seconds):
    if (isinstance(seconds, int)) and (seconds >= 1):
        return True
    else:
        log.error('Invalid integer used. Time to retry should be 1 or more seconds.')
        return False


def valid_dates(startdate, enddate):
    regex = '^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
    if (re.search(regex, startdate) and re.search(regex, enddate)):
        return True
    else:
        log.error('Invalid date format used. Please use "yyyy-mm-dd".')
        return False