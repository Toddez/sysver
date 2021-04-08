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

def assert_response_payload(response_data, payload):
    assert isinstance(response_data, dict)
    for key, value in payload.items():
        assert str(response_data[key]) == value

def assert_response_has_id(response_data):
    assert isinstance(response_data["ID"], int)
    assert response_data["ID"] > 0

class TestRestAPI:
    def test_create_customer(self, db_setup, create_customer):
        payload, response = create_customer

        assert response.ok
        assert response.status_code == 201

        response_data = response.json()
        assert_response_payload(response_data, payload)
        assert_response_has_id(response_data)

        assert response_data["IMEIPtr"] == None
        assert response_data["IMSIPtr"] == None

    def test_create_sim(self, db_setup, create_sim):
        payload, response = create_sim

        assert response.ok
        assert response.status_code == 201

        response_data = response.json()
        assert_response_payload(response_data, payload)
        assert_response_has_id(response_data)

    def test_update_customer_sim(self, db_setup, create_customer, create_sim):
        customer_payload, customer_response = create_customer
        customer_id = customer_response.json()["ID"]

        _, sim_response = create_sim
        sim_id = sim_response.json()["ID"]

        customer_payload["IMSIPtr"] = str(sim_id)

        response = requests.put("http://localhost:6399/customers/" + str(customer_id), json=customer_payload)

        assert response.ok
        assert response.status_code == 200

        response_data = response.json()
        assert_response_payload(response_data, customer_payload)

    def test_create_equipment(self, db_setup, create_equipment):
        payload, response = create_equipment

        assert response.ok
        assert response.status_code == 201

        response_data = response.json()
        assert_response_payload(response_data, payload)
        assert_response_has_id(response_data)

    def test_update_customer_equipment(self, db_setup, create_customer, create_equipment):
        customer_payload, customer_response = create_customer
        customer_id = customer_response.json()["ID"]

        _, equipment_response = create_equipment
        equipment_id = equipment_response.json()["ID"]

        customer_payload["IMEIPtr"] = str(equipment_id)

        response = requests.put("http://localhost:6399/customers/" + str(customer_id), json=customer_payload)

        assert response.ok
        assert response.status_code == 200

        response_data = response.json()
        assert_response_payload(response_data, customer_payload)
