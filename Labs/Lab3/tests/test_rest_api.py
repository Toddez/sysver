import requests
import shutil
import pytest
from fixtures import db_setup, create_customer, create_sim, create_equipment

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
