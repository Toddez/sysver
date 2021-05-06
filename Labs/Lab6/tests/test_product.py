import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

def get_product(id = 1010):
    return requests.get(api_url + "products/" + str(id))

def delete_product(id = 1010):
    return requests.delete(api_url + "products/" + str(id))

def create_product(
    model = "Google Pixel 2 XL",
    product_type = "Phone"
):
    payload = {
        "Model": model,
        "Type": product_type
    }
    return requests.post(api_url + "products", json=payload)

def update_product(
    model = "Google Pixel 2 XL",
    product_type = "Phone"
):
    payload = {
        "Model": model,
        "Type": product_type
    }
    product_id = create_product().json()["ID"]
    return requests.put(api_url + "products/" + str(product_id), json=payload)

def get_product_image(id = 1010):
    return requests.get(api_url + "products/images" + str(id) + ".jpeg")

def update_product_image(
    id = 1010,
    image = b"SOME BINARY DATA"
):
    return requests.put(api_url + "products/" + str(id) + "/image", data=image)

class TestGetProductImage:
    """
    GET: /products/images/<int:id>
    Attempt to get product image with different inputs and check if system crashes
    """

    def test_get_product_image_default(self, db_setup):
        res = get_product_image()
        assert res.status_code != 500

    def test_get_product_image_none_id(self, db_setup):
        res = get_product_image(id=None)
        assert res.status_code != 500

    def test_get_product_image_negative_id(self, db_setup):
        res = get_product_image(id=-1)
        assert res.status_code != 500

    def test_get_product_image_zero_id(self, db_setup):
        res = get_product_image(id=0)
        assert res.status_code != 500

    def test_get_product_image_above_max_id(self, db_setup):
        res = get_product_image(id=pow(2, 63))
        assert res.status_code != 500

    def test_get_product_image_below_min_id(self, db_setup):
        res = get_product_image(id=-pow(2, 63) - 1)
        assert res.status_code != 500

class TestUpdateProductImage:
    """
    PUT: /products/<int:id>/image
    Attempt to update product image with different inputs and check if system crashes
    """

    def test_update_product_image_default(self, db_setup):
        res = update_product_image()
        assert res.status_code != 500

    def test_update_product_image_none_id(self, db_setup):
        res = update_product_image(id=None)
        assert res.status_code != 500

    def test_update_product_image_negative_id(self, db_setup):
        res = update_product_image(id=-1)
        assert res.status_code != 500

    def test_update_product_image_zero_id(self, db_setup):
        res = update_product_image(id=0)
        assert res.status_code != 500

    def test_update_product_image_above_max_id(self, db_setup):
        res = update_product_image(id=pow(2, 63))
        assert res.status_code != 500

    def test_update_product_image_below_min_id(self, db_setup):
        res = update_product_image(id=-pow(2, 63) - 1)
        assert res.status_code != 500

    def test_update_product_image_none_image(self, db_setup):
        res = update_product_image(image=None)
        assert res.status_code != 500

class TestGetProduct:
    """
    GET: /products/<int:id>
    Attempt to get product with different inputs and check if system crashes
    """

    def test_get_product_default(self, db_setup):
        res = get_product()
        assert res.status_code != 500

    def test_get_product_none_id(self, db_setup):
        res = get_product(id=None)
        assert res.status_code != 500

    def test_get_product_negative_id(self, db_setup):
        res = get_product(id=-1)
        assert res.status_code != 500

    def test_get_product_zero_id(self, db_setup):
        res = get_product(id=0)
        assert res.status_code != 500

    def test_get_product_above_max_id(self, db_setup):
        res = get_product(id=pow(2, 63))
        assert res.status_code != 500

    def test_get_product_below_min_id(self, db_setup):
        res = get_product(id=-pow(2, 63) - 1)
        assert res.status_code != 500

class TestDeleteProduct:
    """
    DELETE: /products/<int:id>
    Attempt to delete product with different inputs and check if system crashes
    """

    def test_delete_product_default(self, db_setup):
        res = delete_product()
        assert res.status_code != 500

    def test_delete_product_none_id(self, db_setup):
        res = delete_product(id=None)
        assert res.status_code != 500

    def test_delete_product_negative_id(self, db_setup):
        res = delete_product(id=-1)
        assert res.status_code != 500

    def test_delete_product_zero_id(self, db_setup):
        res = delete_product(id=0)
        assert res.status_code != 500

    def test_delete_product_above_max_id(self, db_setup):
        res = delete_product(id=pow(2, 63))
        assert res.status_code != 500

    def test_delete_product_below_min_id(self, db_setup):
        res = delete_product(id=-pow(2, 63) - 1)
        assert res.status_code != 500

class TestCreateProduct:
    """
    POST: /products/<int:id>
    Attempt to create product with different inputs and check if system crashes
    """

    def test_create_product_default(self, db_setup):
        res = create_product()
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
    """
    PUT: /products/<int:id>
    Attempt to update product with different inputs and check if system crashes
    """

    def test_update_product_default(self, db_setup):
        res = update_product()
        assert res.status_code != 500

    def test_update_product_none_model(self, db_setup):
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
