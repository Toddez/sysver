import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

def get_equipment(id = 380):
    return requests.get(api_url + "equipments/" + str(id))

def delete_equipment(id = 380):
    return requests.delete(api_url + "equipments/" + str(id))

def create_equipment(
    imei = "IMEI_0123456789",
    product_ptr = "1010"
):
    payload = {
        "IMEI": imei,
        "ProductPtr": product_ptr
    }
    return requests.post(api_url + "equipments", json=payload)

def update_equipment(
    imei = "IMEI_0123456789",
    product_ptr = "1010"
):
    payload = {
        "IMEI": imei,
        "ProductPtr": product_ptr
    }
    equipment_id = create_equipment().json()["ID"]
    return requests.put(api_url + "equipments/" + str(equipment_id), json=payload)

class TestGetEquipment:
    """
    GET: /equipments/<int:id>
    Attempt to get equipment with different inputs and check if system crashes
    """

    def test_get_equipment_default(self, db_setup):
        res = get_equipment()
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_equipment_none_id(self, db_setup):
        res = get_equipment(id=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_equipment_negative_id(self, db_setup):
        res = get_equipment(id=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_equipment_zero_id(self, db_setup):
        res = get_equipment(id=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_equipment_above_max_id(self, db_setup):
        res = get_equipment(id=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_get_equipment_below_min_id(self, db_setup):
        res = get_equipment(id=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestDeleteEquipment:
    """
    DELETE: /equipments/<int:id>
    Attempt to delete equipment with different inputs and check if system crashes
    """

    def test_delete_equipment_default(self, db_setup):
        res = delete_equipment()
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_equipment_none_id(self, db_setup):
        res = delete_equipment(id=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_equipment_negative_id(self, db_setup):
        res = delete_equipment(id=-1)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_equipment_zero_id(self, db_setup):
        res = delete_equipment(id=0)
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_equipment_above_max_id(self, db_setup):
        res = delete_equipment(id=pow(2, 63))
        assert res.status_code != 500, 'API failed to handle request'

    def test_delete_equipment_below_min_id(self, db_setup):
        res = delete_equipment(id=-pow(2, 63) - 1)
        assert res.status_code != 500, 'API failed to handle request'

class TestCreateEquipment:
    """
    POST: /equipments
    Attempt to create equipment with different inputs and check if system crashes
    """

    def test_create_equipment_default(self, db_setup):
        res = create_equipment()
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_none_imei(self, db_setup):
        res = create_equipment(imei=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_long_imei(self, db_setup):
        res = create_equipment(imei="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_non_ascii_imei(self, db_setup):
        res = create_equipment(imei="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_none_product_ptr(self, db_setup):
        res = create_equipment(product_ptr=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_long_product_ptr(self, db_setup):
        res = create_equipment(product_ptr="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_create_equipment_non_ascii_product_ptr(self, db_setup):
        res = create_equipment(product_ptr="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

class TestUpdateEquipment:
    """
    PUT: /equipments/<int:id>
    Attempt to update equipment with different inputs and check if system crashes
    """

    def test_update_equipment_default(self, db_setup):
        res = update_equipment()
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_none_imei(self, db_setup):
        res = update_equipment(imei=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_long_imei(self, db_setup):
        res = update_equipment(imei="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_non_ascii_imei(self, db_setup):
        res = update_equipment(imei="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_none_product_ptr(self, db_setup):
        res = update_equipment(product_ptr=None)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_long_product_ptr(self, db_setup):
        res = update_equipment(product_ptr="A"*51)
        assert res.status_code != 500, 'API failed to handle request'

    def test_update_equipment_non_ascii_product_ptr(self, db_setup):
        res = update_equipment(product_ptr="åäö😀")
        assert res.status_code != 500, 'API failed to handle request'

