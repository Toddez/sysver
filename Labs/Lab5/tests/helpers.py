from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
seconds_to_wait = 4

def assert_input(driver, data):
    # assert data
    for id, value in data.items():
        input_element = driver.find_element_by_id(id)
        assert input_element.is_enabled() == False
        assert input_element.get_attribute("value") == str(value)

def open_customer(driver, customer):
    # find customer and click
    customer_element = driver.find_element_by_id(customer["ID"])
    customer_element.click()

    # make sure the non-input fiels have the correct values
    image_element = driver.find_element_by_xpath("/html/body/div/div/div[4]/table/tbody/tr[1]/td[3]/img")
    assert customer["equipment"]["product"]["ImageURL"] in image_element.get_attribute("src")

    device_element = driver.find_element_by_xpath("/html/body/div/div/div[4]/table/tbody/tr[3]/td[2]")
    assert device_element.get_attribute("innerHTML") == customer["equipment"]["product"]["Model"]

    device_type_element = driver.find_element_by_xpath("/html/body/div/div/div[4]/table/tbody/tr[4]/td[2]")
    assert device_type_element.get_attribute("innerHTML") == customer["equipment"]["product"]["Type"]

    device_imei_element = driver.find_element_by_xpath("/html/body/div/div/div[4]/table/tbody/tr[5]/td[2]")
    assert device_imei_element.get_attribute("innerHTML") == customer["equipment"]["IMEI"]

    # input field values
    data = {
        #customer
        "firstname": customer["Firstname"],
        "lastname": customer["Lastname"],
        "age": customer["Age"],
        "gender": customer["Sex"],
        "nationality": customer["Nationality"],
        "street": customer["Street"],
        "zipcode": customer["Zip"],
        "city": customer["City"],
        "email": customer["Email"],

        # equipment
        "phone": customer["sim"]["MSISDN"],
        "imsi": customer["sim"]["IMSI"]
    }

    # make sure the input fields have the correct data
    assert_input(driver, data)

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

    # wait for save request to finish and trigger reload
    try:
        WebDriverWait(driver, seconds_to_wait).until(EC.staleness_of(driver.find_element_by_xpath("/html/body/div/div/div[1]")))
    except TimeoutException:
        print("Took too long to wait for refresh")

    # wait for page reload and get customer list
    try:
        customer_list_element = WebDriverWait(driver, seconds_to_wait).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]")))
    except TimeoutException:
        print("Loading took too much time!")

    # select the customer
    customer_buttons = customer_list_element.find_elements_by_tag_name("p")
    assert len(customer_buttons) > 0
    edited_customer_button = customer_buttons[len(customer_buttons) - 1]
    edited_customer_button.click()

    assert_input(driver, data)
