import shutil
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

@pytest.fixture()
def db_setup():
    shutil.copy("/home/pft/restapi/point-of-sale/pos_bak.db", "/home/pft/restapi/point-of-sale/pos.db")

def assert_input(driver, data):
    # assert data
    for id, value in data.items():
        input_element = driver.find_element_by_id(id)
        assert input_element.is_enabled() == False
        assert input_element.get_attribute("value") == str(value)

def fill_out_customer_form(driver):
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "age": "42",
        "gender": "Male",
        "nationality": "Swedish",
        "street": "Granvägen",
        "zipcode": "12345",
        "city": "Doetorp",
        "email": "john@doe.com"
    }

    # fill in data
    for id, value in data.items():
        # find element by id
        input_element = driver.find_element_by_id(id)
        assert input_element.is_enabled() == True

        # fill in data
        input_element.clear()
        input_element.send_keys(value)

    # click save
    save_element = driver.find_element_by_id("save_customer_btn")
    save_element.click()

    # wait for page reload and get customer list
    seconds_to_wait = 4
    try:
        customer_list_element = WebDriverWait(driver, seconds_to_wait).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]")))
    except TimeoutException:
        print("Loading took too much time!")

    # select the customer
    customer_buttons = customer_list_element.find_elements_by_tag_name("p")
    edited_customer_button = customer_buttons[-1]
    edited_customer_button.click()

    assert_input(driver, data)

class TestGUI:
    def setup_method(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("http://localhost")
        assert self.driver.title == "Customer Care"

    def teardown_method(self):
        self.driver.close()

    # Test case 1
    def test_open_exisiting_user(self, db_setup):
        result = requests.get("http://localhost:6399/customers")
        assert result.ok
        assert result.status_code == 200

        customers = result.json()
        assert len(customers) > 0

        customer = customers[0]
        assert customer is not None

        # select customer
        customer_element = self.driver.find_element_by_id(customer["ID"])
        customer_element.click()

        data = {
            "firstname": customer["Firstname"],
            "lastname": customer["Lastname"],
            "age": customer["Age"],
            "gender": customer["Sex"],
            "nationality": customer["Nationality"],
            "street": customer["Street"],
            "zipcode": customer["Zip"],
            "city": customer["City"],
            "email": customer["Email"],
        }
        assert_input(self.driver, data)

        # click edit
        edit_element = self.driver.find_element_by_id("edit_customer_btn")
        edit_element.click()

        fill_out_customer_form(self.driver)

    def test_create_customer(self, db_setup):
        # click create new customer button
        create_element = self.driver.find_element_by_xpath("/html/body/div/div/div[1]/button")
        create_element.click()

        fill_out_customer_form(self.driver)

# TODO: More test cases that cover the critical paths in the system
# TODO: Removing customer.
