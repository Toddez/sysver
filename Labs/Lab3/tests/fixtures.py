import requests
import shutil
import pytest
from test_rest_api import api_url

# path should probably be an environment variable
db_path = "/home/pft/restapi/point-of-sale/"

@pytest.fixture()
def db_setup():
    shutil.copy(db_path + "pos_bak.db", db_path + "pos.db")

@pytest.fixture()
def create_customer(data=None):
    payload = {
        "Firstname": "John",
        "Lastname": "Doe",
        "Age": "42",
        "Sex": "Male",
        "Street": "Granvägen",
        "Zip": "12345",
        "City": "Doetorp",
        "Nationality": "Swedish",
        "Email": "john@doe.com",
        "Password": "z3CretP4ssW0rd"
    }

    if isinstance(data, dict):
        payload = data

    return (
        payload,
        requests.post(api_url + "customers", json=payload)
    )

@pytest.fixture()
def create_sim():
    payload = {
        "IMSI": "IMSI_0123456789",
        "MSISDN": "+46712345678"
    }
    return (
        payload,
        requests.post(api_url + "sims", json=payload)
    )

@pytest.fixture()
def create_equipment():
    # fetch product from database -> get id
    response = requests.get(api_url + "products")
    product_id = response.json()[0]["ID"]

    # create equipment with product id
    payload = {
        "IMEI": "IMEI_336699",
        "ProductPtr": str(product_id)
    }
    return (
        payload,
        requests.post(api_url + "equipments", json=payload)
    )
