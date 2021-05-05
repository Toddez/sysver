import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

def create_product(
    image_url = "/products/images/1010.jpeg",
    model = "Google Pixel 2 XL",
    product_type = "Phone"
):
    payload = {
        "ImageURL": image_url,
        "Model": model,
        "Type": product_type
    }
    return requests.post(api_url + "products", json=payload)

def update_product(
    image_url = "/products/images/1010.jpeg",
    model = "Google Pixel 2 XL",
    product_type = "Phone"
):
    payload = {
        "ImageURL": image_url,
        "Model": model,
        "Type": product_type
    }
    product_id = create_product().json()["ID"]
    return requests.put(api_url + "products/" + str(product_id), json=payload)

class TestCreateProduct:
    def test_create_product_default(self, db_setup):
        res = create_product()
        assert res.status_code != 500

    def test_create_product_none_image(self, db_setup):
        res = create_product(image_url=None)
        assert res.status_code != 500

    def test_create_product_long_image(self, db_setup):
        res = create_product(image_url="A"*51)
        assert res.status_code != 500

    def test_create_product_non_ascii_image(self, db_setup):
        res = create_product(image_url="åäö😀")
        assert res.status_code != 500

    def test_create_product_none_model(self, db_setup):
        res = create_product(model=None)
        assert res.status_code != 500

    def test_create_product_long_model(self, db_setup):
        res = create_product(model="A"*51)
        assert res.status_code != 500

    def test_create_product_non_ascii_model(self, db_setup):
        res = create_product(model="åäö😀")
        assert res.status_code != 500

    def test_create_product_none_type(self, db_setup):
        res = create_product(product_type=None)
        assert res.status_code != 500

    def test_create_product_long_type(self, db_setup):
        res = create_product(product_type="A"*51)
        assert res.status_code != 500

    def test_create_product_non_ascii_type(self, db_setup):
        res = create_product(product_type="åäö😀")
        assert res.status_code != 500

class TestUpdateProduct:
    def test_update_product_default(self, db_setup):
        res = update_product()
        assert res.status_code != 500

    def test_update_product_none_image(self, db_setup):
        res = update_product(image_url=None)
        assert res.status_code != 500

    def test_update_product_long_image(self, db_setup):
        res = update_product(image_url="A"*51)
        assert res.status_code != 500

    def test_update_product_non_ascii_image(self, db_setup):
        res = update_product(image_url="åäö😀")
        assert res.status_code != 500

    def test_update_prodct_none_model(self, db_setup):
        res = update_product(model=None)
        assert res.status_code != 500

    def test_update_product_long_model(self, db_setup):
        res = update_product(model="A"*51)
        assert res.status_code != 500

    def test_update_product_non_ascii_model(self, db_setup):
        res = update_product(model="åäö😀")
        assert res.status_code != 500

    def test_update_product_none_type(self, db_setup):
        res = update_product(product_type=None)
        assert res.status_code != 500

    def test_update_product_long_type(self, db_setup):
        res = update_product(product_type="A"*51)
        assert res.status_code != 500

    def test_update_product_non_ascii_type(self, db_setup):
        res = update_product(product_type="åäö😀")
        assert res.status_code != 500
