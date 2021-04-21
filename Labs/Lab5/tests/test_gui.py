import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from fixtures import db_setup, driver_setup, get_customer
from helpers import assert_input, fill_out_customer_form, open_customer

seconds_to_wait = 4

class TestGUI:
    def test_open_exisiting_customer(self, db_setup, driver_setup, get_customer):
        driver = driver_setup

        # get a customer to open
        customer = get_customer

        # open customer and assert input
        open_customer(driver, customer)

        driver.close()

    def test_create_customer(self, db_setup, driver_setup):
        driver = driver_setup

        # click create new customer button
        create_element = driver.find_element_by_xpath("/html/body/div/div/div[1]/button")
        create_element.click()

        # fill out customer form, save and assert input
        fill_out_customer_form(driver)

        driver.close()

    def test_edit_customer(self, db_setup, driver_setup, get_customer):
        driver = driver_setup

        # get a customer to edit
        customer = get_customer

        # open customer and assert input
        open_customer(driver, customer)

        # click edit
        edit_element = driver.find_element_by_id("edit_customer_btn")
        edit_element.click()

        # fill out customer form, save and assert input
        fill_out_customer_form(driver)

        driver.close()

    def test_delete_customer(self, db_setup, driver_setup):
        driver = driver_setup

        # find all customers
        customer_list_element = driver.find_element_by_xpath("/html/body/div/div/div[1]")
        customer_elements = customer_list_element.find_elements_by_tag_name("p")
        customer_count = len(customer_elements)
        assert customer_count > 0

        # select first customer
        customer_element = customer_elements[0]
        customer_id = customer_element.get_attribute("id")
        customer_element.click()

        # click delete
        delete_element = driver.find_element_by_id("delete_customer_btn")
        delete_element.click()

        # click confirm
        alert = driver.switch_to.alert
        assert alert.text == "Are you sure you want to delete this customer?"
        alert.accept()

        # wait for save request to finish and trigger reload
        try:
            WebDriverWait(driver, seconds_to_wait).until(EC.staleness_of(customer_list_element))
        except TimeoutException:
            print("Took too long to wait for refresh")

        # wait for vue to render, the v-for div should be removed when done
        try:
            customer_list_is_empty = WebDriverWait(driver, seconds_to_wait).until_not(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div[1]")))
        except TimeoutException:
            print("Took too long to find customer_list_element")

        # confirm the user was deleted
        customer_elements = driver.find_element_by_xpath("/html/body/div/div/div[1]").find_elements_by_tag_name("p")
        assert len(customer_elements) < customer_count
        assert len(driver.find_elements_by_id(customer_id)) == 0
        assert customer_list_is_empty == True

        driver.close()
