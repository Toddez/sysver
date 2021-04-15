import requests
import shutil
import pytest

@pytest.fixture()
def db_setup():
    shutil.copy("/home/pft/restapi/point-of-sale/pos_bak.db", "/home/pft/restapi/point-of-sale/pos.db")

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
        requests.post("http://localhost:6399/customers", json=payload)
    )

@pytest.fixture()
def create_sim():
    payload = {
        "IMSI": "IMSI_0123456789",
        "MSISDN": "+46712345678"
    }
    return (
        payload,
        requests.post("http://localhost:6399/sims", json=payload)
    )

@pytest.fixture()
def create_equipment():
    # fetch product from database -> get id
    response = requests.get("http://localhost:6399/products")
    product_id = response.json()[0]["ID"]

    # create equipment with product id
    payload = {
        "IMEI": "IMEI_336699",
        "ProductPtr": str(product_id)
    }
    return (
        payload,
        requests.post("http://localhost:6399/equipments", json=payload)
    )
