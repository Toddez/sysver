import shutil
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

@pytest.fixture()
def db_setup():
    """
    Restores the database from a backup
    """

    shutil.copy("/home/pft/restapi/point-of-sale/pos_bak.db", "/home/pft/restapi/point-of-sale/pos.db")

@pytest.fixture()
def driver_setup():
    """
    Opens and returns a headless driver and opens localhost
    """

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://localhost")

    yield driver

    driver.close()

@pytest.fixture()
def get_customer():
    """
    Fetches and returns the first customer from the API.
    Since we know the state of the database,
    we can assume that there is always at least one customer.
    We first send an API request to get all customers,
    and then another to get the full information about the first one
    """

    # get all customers and pick first one
    customers_result = requests.get("http://localhost:6399/customers")
    customer_id = customers_result.json()[0]["ID"]

    # get full info about customer
    result = requests.get("http://localhost:6399/full_customer/" + str(customer_id))

    return result.json()
