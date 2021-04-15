import shutil
import pytest
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
