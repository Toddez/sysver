import shutil
import pytest
import sqlite3
import subprocess

# path should probably be an environment variable
db_path = "/home/pft/restapi/point-of-sale/"

@pytest.fixture()
def db_setup():

    try:
        process = int(subprocess.check_output(["fuser", db_path + "pos.db"]))
    except:
        process = None

    # if database is locked, remove it
    if process is not None:
        subprocess.check_call(["rm", db_path + "pos.db"])

    shutil.copy(db_path + "pos_bak.db", db_path + "pos.db")
