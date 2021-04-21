import shutil
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

@pytest.fixture()
def db_setup():
    shutil.copy("/home/pft/restapi/point-of-sale/pos_bak.db", "/home/pft/restapi/point-of-sale/pos.db")

@pytest.fixture()
def driver_setup():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://localhost")
    assert driver.title == "Customer Care"
    return driver

@pytest.fixture()
def get_customer():
    result = requests.get("http://localhost:6399/full_customer/513")
    assert result.ok
    assert result.status_code == 200

    customer = result.json()
    assert customer is not None

    return customer
