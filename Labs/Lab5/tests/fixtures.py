import shutil
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

@pytest.fixture()
def db_setup():
    """
    Restores the database to a backup.
    """

    shutil.copy("/home/pft/restapi/point-of-sale/pos_bak.db", "/home/pft/restapi/point-of-sale/pos.db")

@pytest.fixture()
def driver_setup():
    """
    Opens and returns a headless driver and opens localhost.
    """

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://localhost")

    return driver

@pytest.fixture()
def get_customer():
    """
    Fetches and returns known customer data from the API.
    Since we know the state of the database, we can use a hard-coded customer.
    """

    result = requests.get("http://localhost:6399/full_customer/513")

    return result.json()
