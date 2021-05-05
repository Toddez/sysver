import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

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

class TestCreateEquipment:
    def test_create_equipment_default(self, db_setup):
        res = create_equipment()
        assert res.status_code != 500

    def test_create_equipment_none_imei(self, db_setup):
        res = create_equipment(imei=None)
        assert res.status_code != 500

    def test_create_equipment_long_imei(self, db_setup):
        res = create_equipment(imei="A"*51)
        assert res.status_code != 500

    def test_create_equipment_non_ascii_imei(self, db_setup):
        res = create_equipment(imei="åäö😀")
        assert res.status_code != 500

    def test_create_equipment_none_product_ptr(self, db_setup):
        res = create_equipment(product_ptr=None)
        assert res.status_code != 500

    def test_create_equipment_long_product_ptr(self, db_setup):
        res = create_equipment(product_ptr="A"*51)
        assert res.status_code != 500

    def test_create_equipment_non_ascii_product_ptr(self, db_setup):
        res = create_equipment(product_ptr="åäö😀")
        assert res.status_code != 500

class TestUpdateEquipment:
    def test_update_equipment_default(self, db_setup):
        res = update_equipment()
        assert res.status_code != 500

    def test_update_equipment_none_imei(self, db_setup):
        res = update_equipment(imei=None)
        assert res.status_code != 500

    def test_update_equipment_long_imei(self, db_setup):
        res = update_equipment(imei="A"*51)
        assert res.status_code != 500

    def test_update_equipment_non_ascii_imei(self, db_setup):
        res = update_equipment(imei="åäö😀")
        assert res.status_code != 500

    def test_update_equipment_none_product_ptr(self, db_setup):
        res = update_equipment(product_ptr=None)
        assert res.status_code != 500

    def test_update_equipment_long_product_ptr(self, db_setup):
        res = update_equipment(product_ptr="A"*51)
        assert res.status_code != 500

    def test_update_equipment_non_ascii_product_ptr(self, db_setup):
        res = update_equipment(product_ptr="åäö😀")
        assert res.status_code != 500
