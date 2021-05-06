import requests
import shutil
import pytest

from fixtures import db_setup

api_url = "http://localhost:6399/"

def get_customer(id = 513):
    return requests.get(api_url + "customers/" + str(id))

def get_full_customer(id = 513):
    return requests.get(api_url + "full_customer/" + str(id))

def delete_customer(id = 513):
    return requests.delete(api_url + "customers/" + str(id))

def create_customer(
    first_name = "John",
    last_name = "Doe",
    age = 42,
    sex = "M",
    street = "Storgatan",
    zip_code = "12345",
    city = "Doetorp",
    nationality = "Swedish",
    email = "john@doe.com",
    password = "z3CretP4ssW0rd",
    imei = 380,
    imsi = 635
):
    payload = {
        "Firstname": first_name,
        "Lastname": last_name,
        "Age": age,
        "Sex": sex,
        "Street": street,
        "Zip": zip_code,
        "City": city,
        "Nationality": nationality,
        "Email": email,
        "Password": password,
        "IMEIPtr": imei,
        "IMSIPtr": imsi
    }
    return requests.post(api_url + "customers", json=payload)

def update_customer(
    first_name = "John",
    last_name = "Doe",
    age = 42,
    sex = "M",
    street = "Storgatan",
    zip_code = "12345",
    city = "Doetorp",
    nationality = "Swedish",
    email = "john@doe.com",
    password = "z3CretP4ssW0rd",
    imei = 635,
    imsi = 380
):
    payload = {
        "Firstname": first_name,
        "Lastname": last_name,
        "Age": age,
        "Sex": sex,
        "Street": street,
        "Zip": zip_code,
        "City": city,
        "Nationality": nationality,
        "Email": email,
        "Password": password,
        "IMEIPtr": imei,
        "IMSIPtr": imsi
    }
    customer_id = create_customer().json()["ID"]
    return requests.put(api_url + "customers/" + str(customer_id), json=payload)

class TestGetCustomer:
    """
    GET: /customers/<int:id>
    Attempt to get customer with different inputs and check if system crashes
    """

    def test_get_customer_default(self, db_setup):
        res = get_customer()
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_customer_none_id(self, db_setup):
        res = get_customer(id=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_customer_negative_id(self, db_setup):
        res = get_customer(id=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_customer_zero_id(self, db_setup):
        res = get_customer(id=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_customer_above_max_id(self, db_setup):
        res = get_customer(id=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_customer_below_min_id(self, db_setup):
        res = get_customer(id=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestGetFullCustomer:
    """
    GET: /full_customer/<int:id>
    Attempt to get full customer with different inputs and check if system crashes
    """

    def test_get_full_customer_default(self, db_setup):
        res = get_full_customer()
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_full_customer_none_id(self, db_setup):
        res = get_full_customer(id=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_full_customer_negative_id(self, db_setup):
        res = get_full_customer(id=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_full_customer_zero_id(self, db_setup):
        res = get_full_customer(id=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_full_customer_above_max_id(self, db_setup):
        res = get_full_customer(id=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_full_customer_below_min_id(self, db_setup):
        res = get_full_customer(id=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestDeleteCustomer:
    """
    DELETE: /customers/<int:id>
    Attempt to delete customer with different inputs and check if system crashes
    """

    def test_delete_customer_default(self, db_setup):
        res = delete_customer()
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_customer_none_id(self, db_setup):
        res = delete_customer(id=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_customer_negative_id(self, db_setup):
        res = delete_customer(id=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_customer_zero_id(self, db_setup):
        res = delete_customer(id=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_customer_above_max_id(self, db_setup):
        res = delete_customer(id=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_customer_below_min_id(self, db_setup):
        res = delete_customer(id=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestCreateCustomer:
    """
    POST: /customers
    Attempt to create customer with different inputs and check if system crashes
    """

    def test_create_customer_default(self, db_setup):
        res = create_customer()
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_firstname(self, db_setup):
        res = create_customer(first_name=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_firstname(self, db_setup):
        res = create_customer(first_name="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_firstname(self, db_setup):
        res = create_customer(first_name="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_lastname(self, db_setup):
        res = create_customer(last_name=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_lastname(self, db_setup):
        res = create_customer(last_name="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_lastname(self, db_setup):
        res = create_customer(last_name="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_age(self, db_setup):
        res = create_customer(age=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_string_age(self, db_setup):
        res = create_customer(age="1")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_float_age(self, db_setup):
        res = create_customer(age=1.5)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_negative_age(self, db_setup):
        res = create_customer(age=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_zero_age(self, db_setup):
        res = create_customer(age=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_above_max_age(self, db_setup):
        res = create_customer(age=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_below_min_age(self, db_setup):
        res = create_customer(age=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_sex(self, db_setup):
        res = create_customer(sex=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_sex(self, db_setup):
        res = create_customer(sex="A"*11)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_sex(self, db_setup):
        res = create_customer(sex="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_street(self, db_setup):
        res = create_customer(street=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_street(self, db_setup):
        res = create_customer(street="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_street(self, db_setup):
        res = create_customer(street="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_zip(self, db_setup):
        res = create_customer(zip_code=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_zip(self, db_setup):
        res = create_customer(zip_code="A"*11)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_zip(self, db_setup):
        res = create_customer(zip_code="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_city(self, db_setup):
        res = create_customer(city=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_city(self, db_setup):
        res = create_customer(city="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_city(self, db_setup):
        res = create_customer(city="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_nationality(self, db_setup):
        res = create_customer(nationality=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_nationality(self, db_setup):
        res = create_customer(nationality="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_nationality(self, db_setup):
        res = create_customer(nationality="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_email(self, db_setup):
        res = create_customer(email=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_email(self, db_setup):
        res = create_customer(email="A"*101)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_email(self, db_setup):
        res = create_customer(email="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_password(self, db_setup):
        res = create_customer(password=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_long_password(self, db_setup):
        res = create_customer(password="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_non_ascii_password(self, db_setup):
        res = create_customer(password="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_imei(self, db_setup):
        res = create_customer(imei=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_negative_imei(self, db_setup):
        res = create_customer(imei=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_zero_imei(self, db_setup):
        res = create_customer(imei=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_above_max_imei(self, db_setup):
        res = create_customer(imei=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_below_min_imei(self, db_setup):
        res = create_customer(imei=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_none_imsi(self, db_setup):
        res = create_customer(imsi=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_negative_imsi(self, db_setup):
        res = create_customer(imsi=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_zero_imsi(self, db_setup):
        res = create_customer(imsi=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_above_max_imsi(self, db_setup):
        res = create_customer(imsi=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_customer_below_min_imsi(self, db_setup):
        res = create_customer(imsi=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestUpdateCustomer:
    """
    PUT: /customers/<int:id>
    Attempt to update customer with different inputs and check if system crashes
    """

    def test_update_customer_default(self, db_setup):
        res = update_customer()
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_firstname(self, db_setup):
        res = update_customer(first_name=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_firstname(self, db_setup):
        res = update_customer(first_name="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_non_ascii_firstname(self, db_setup):
        res = update_customer(first_name="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_lastname(self, db_setup):
        res = update_customer(last_name=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_lastname(self, db_setup):
        res = update_customer(last_name="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_age(self, db_setup):
        res = update_customer(age=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_string_age(self, db_setup):
        res = update_customer(age="1")
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_float_age(self, db_setup):
        res = update_customer(age=1.5)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_negative_age(self, db_setup):
        res = update_customer(age=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_zero_age(self, db_setup):
        res = update_customer(age=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_above_max_age(self, db_setup):
        res = update_customer(age=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_below_min_age(self, db_setup):
        res = update_customer(age=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_sex(self, db_setup):
        res = update_customer(sex=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_sex(self, db_setup):
        res = update_customer(sex="A"*11)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_street(self, db_setup):
        res = update_customer(street=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_street(self, db_setup):
        res = update_customer(street="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_zip(self, db_setup):
        res = update_customer(zip_code=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_zip(self, db_setup):
        res = update_customer(zip_code="A"*11)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_city(self, db_setup):
        res = update_customer(city=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_city(self, db_setup):
        res = update_customer(city="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_nationality(self, db_setup):
        res = update_customer(nationality=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_nationality(self, db_setup):
        res = update_customer(nationality="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_email(self, db_setup):
        res = update_customer(email=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_email(self, db_setup):
        res = update_customer(email="A"*101)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_password(self, db_setup):
        res = update_customer(password=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_long_password(self, db_setup):
        res = update_customer(password="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_imei(self, db_setup):
        res = update_customer(imei=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_negative_imei(self, db_setup):
        res = update_customer(imei=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_zero_imei(self, db_setup):
        res = update_customer(imei=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_above_max_imei(self, db_setup):
        res = update_customer(imei=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_below_min_imei(self, db_setup):
        res = update_customer(imei=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_none_imsi(self, db_setup):
        res = update_customer(imsi=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_negative_imsi(self, db_setup):
        res = update_customer(imsi=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_zero_imsi(self, db_setup):
        res = update_customer(imsi=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_above_max_imsi(self, db_setup):
        res = update_customer(imsi=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_customer_below_min_imsi(self, db_setup):
        res = update_customer(imsi=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

