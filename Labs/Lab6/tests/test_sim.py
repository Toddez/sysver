import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

def get_sim(id = 635):
    return requests.get(api_url + "sims/" + str(id))

def delete_sim(id = 635):
    return requests.delete(api_url + "sims/" + str(id))

def create_sim(
    imsi = "IMSI_0123456789",
    msisdn = "+46723580953"
):
    payload = {
        "IMSI": imsi,
        "MSISDN": msisdn
    }
    return requests.post(api_url + "sims", json=payload)

def update_sim(
    imsi = "IMSI_0123456789",
    msisdn = "+46723580953"
):
    payload = {
        "IMSI": imsi,
        "MSISDN": msisdn
    }
    sim_id = create_sim().json()["ID"]
    return requests.put(api_url + "sims/" + str(sim_id), json=payload)

class TestGetSim:
    """
    GET: /sims/<int:id>
    Attempt to get sim with different inputs and check if system crashes
    """

    def test_get_sim_default(self, db_setup):
        res = get_sim()
        assert res.status_code != 500

    def test_get_sim_none_id(self, db_setup):
        res = get_sim(id=None)
        assert res.status_code != 500

    def test_get_sim_negative_id(self, db_setup):
        res = get_sim(id=-1)
        assert res.status_code != 500

    def test_get_sim_zero_id(self, db_setup):
        res = get_sim(id=0)
        assert res.status_code != 500

    def test_get_sim_above_max_id(self, db_setup):
        res = get_sim(id=pow(2, 63))
        assert res.status_code != 500

    def test_get_sim_below_min_id(self, db_setup):
        res = get_sim(id=-pow(2, 63) - 1)
        assert res.status_code != 500

class TestDeleteSim:
    """
    DELETE: /sims/<int:id>
    Attempt to delet sim with different inputs and check if system crashes
    """

    def test_delete_sim_default(self, db_setup):
        res = delete_sim()
        assert res.status_code != 500

    def test_delete_sim_none_id(self, db_setup):
        res = delete_sim(id=None)
        assert res.status_code != 500

    def test_delete_sim_negative_id(self, db_setup):
        res = delete_sim(id=-1)
        assert res.status_code != 500

    def test_delete_sim_zero_id(self, db_setup):
        res = delete_sim(id=0)
        assert res.status_code != 500

    def test_delete_sim_above_max_id(self, db_setup):
        res = delete_sim(id=pow(2, 63))
        assert res.status_code != 500

    def test_delete_sim_below_min_id(self, db_setup):
        res = delete_sim(id=-pow(2, 63) - 1)
        assert res.status_code != 500

class TestCreateSim:
    """
    POST: /sims/<int:id>
    Attempt to create sim with different inputs and check if system crashes
    """

    def test_create_sim_default(self, db_setup):
        res = create_sim()
        assert res.status_code != 500

    def test_create_sim_none_imsi(self, db_setup):
        res = create_sim(imsi=None)
        assert res.status_code != 500

    def test_create_sim_long_imsi(self, db_setup):
        res = create_sim(imsi="A"*51)
        assert res.status_code != 500

    def test_create_sim_non_ascii_imsi(self, db_setup):
        res = create_sim(imsi="åäö😀")
        assert res.status_code != 500

    def test_create_sim_none_msisdn(self, db_setup):
        res = create_sim(msisdn=None)
        assert res.status_code != 500

    def test_create_sim_long_msisdn(self, db_setup):
        res = create_sim(msisdn="A"*51)
        assert res.status_code != 500

    def test_create_sim_non_ascii_msisdn(self, db_setup):
        res = create_sim(msisdn="åäö😀")
        assert res.status_code != 500

class TestUpdateSim:
    """
    PUT: /sims/<int:id>
    Attempt to update sim with different inputs and check if system crashes
    """

    def test_update_sim_default(self, db_setup):
        res = update_sim()
        assert res.status_code != 500

    def test_update_sim_none_imsi(self, db_setup):
        res = update_sim(imsi=None)
        assert res.status_code != 500

    def test_update_sim_long_imsi(self, db_setup):
        res = update_sim(imsi="A"*51)
        assert res.status_code != 500

    def test_update_sim_non_ascii_imsi(self, db_setup):
        res = update_sim(imsi="åäö😀")
        assert res.status_code != 500

    def test_update_sim_none_msisdn(self, db_setup):
        res = update_sim(msisdn=None)
        assert res.status_code != 500

    def test_update_sim_long_msisdn(self, db_setup):
        res = update_sim(msisdn="A"*51)
        assert res.status_code != 500

    def test_update_sim_non_ascii_msisdn(self, db_setup):
        res = update_sim(msisdn="åäö😀")
        assert res.status_code != 500
