import shutil
import pytest
import sqlite3
import subprocess
import warnings

# path should probably be an environment variable
db_path = "/home/pft/restapi/point-of-sale/"

@pytest.fixture()
def db_setup():
    """
    Check if database is locked, and unlock if needed
    Reset database to known state
    """

    # detect zombie process locking the database
    try:
        process = int(subprocess.check_output(["fuser", db_path + "pos.db"]))
    except:
        process = None

    # if database is locked, remove the database to force unlock it
    if process is not None:
        subprocess.check_call(["rm", db_path + "pos.db"])
        warnings.warn("Detected zombie process locking the database")

    # rest database to known state
    shutil.copy(db_path + "pos_bak.db", db_path + "pos.db")

