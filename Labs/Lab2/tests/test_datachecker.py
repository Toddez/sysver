from datachecker import DataChecker
from unittest.mock import patch

class TestDataChecker:

    @patch.object(DataChecker, "connect_to_database")
    def setup_method(self, method, mocked_connect_to_database):
        self.dc = DataChecker()

    def test_check_valid_age(self):
        dc = self.dc

        assert dc.check_valid_age(1) == True
        assert dc.check_valid_age(-1) == False
        assert dc.check_valid_age(1.5) == False
        assert dc.check_valid_age("one") == False

    def test_check_valid_text_field(self):
        dc = self.dc

        assert dc.check_valid_text_field("") == False
        assert dc.check_valid_text_field("not empty") == True
        assert dc.check_valid_text_field("", False) == True
        assert dc.check_valid_text_field("not empty", False) == True

    @patch.object(DataChecker, "get_customer")
    @patch.object(DataChecker, "get_equipment")
    def test_customer_has_equipment_attached(self, mocked_get_customer, mocked_get_equipment):
        dc = self.dc

        # invalid customer
        dc.get_customer.return_value = []
        assert dc.customer_has_equipment_attached(0) == False

        # valid customer - invalid equipment pointer
        dc.get_customer.return_value = [
            # customer
            [
                0, "", "", 0, "", "", "", "", "", None,
                None, # invalid equipment pointer
                None, "", ""
            ]
        ]
        assert dc.customer_has_equipment_attached(0) == False

        # valid customer - valid equipment pointer - invalid equipment
        dc.get_customer.return_value[0][9] = 0 # Set valid equipment pointer
        dc.get_equipment.return_value = [] # no equipment
        assert dc.customer_has_equipment_attached(0) == False

        # valid customer - valid equipment pointer - valid equipment
        dc.get_customer.return_value[0][9] = 0 # Set valid equipment pointer
        dc.get_equipment.return_value = [
            # some equipment
            []
        ]
        assert dc.customer_has_equipment_attached(0) == True
