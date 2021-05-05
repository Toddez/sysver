import requests
import shutil
import pytest

from test_customer import api_url
from fixtures import db_setup

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

class TestCreateSim:
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
