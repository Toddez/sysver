from datachecker import DataChecker
from unittest.mock import patch

class TestDataChecker:

    @patch.object(DataChecker, "connect_to_database")
    def setup_method(self, method, mocked_connect_to_database):
        self.dc = DataChecker()

    def test_check_valid_age_invalid_type_string(self):
        assert self.dc.check_valid_age("1") == False

    def test_check_valid_age_invalid_type_float(self):
        assert self.dc.check_valid_age(1.5) == False

    def test_check_valid_age_negative_integer_small(self):
        assert self.dc.check_valid_age(-1) == False

    def test_check_valid_age_negative_integer_large(self):
        assert self.dc.check_valid_age(-1000) == False

    def test_check_valid_age_positive_integer_zero(self):
        assert self.dc.check_valid_age(0) == True

    def test_check_valid_age_positive_integer_small(self):
        assert self.dc.check_valid_age(1) == True

    def test_check_valid_age_positive_integer_large(self):
        assert self.dc.check_valid_age(1000) == True

    def test_check_valid_text_field_empty_default(self):
        assert self.dc.check_valid_text_field("") == False

    def test_check_valid_text_field_empty_must_not_have_content(self):
        assert self.dc.check_valid_text_field("", False) == True

    def test_check_valid_text_field_content_default(self):
        assert self.dc.check_valid_text_field("not empty") == True

    def test_check_valid_text_field_content_must_not_have_content(self):
        assert self.dc.check_valid_text_field("not empty", False) == True

    @patch.object(DataChecker, "get_customer")
    def test_customer_has_equipment_attached_invalid_customer(self, mocked_get_customer):
        # invalid customer
        self.dc.get_customer.return_value = []

        assert self.dc.customer_has_equipment_attached(0) == False

    @patch.object(DataChecker, "get_customer")
    def test_customer_has_equipment_attached_valid_customer_invalid_ptr(self, mocked_get_customer):
        # valid customer - no equipment pointer
        self.dc.get_customer.return_value = [
            # customer
            [
                0, "", "", 0, "", "", "", "", "", None,
                None, # invalid equipment pointer
                None, "", ""
            ]
        ]

        assert self.dc.customer_has_equipment_attached(0) == False

    @patch.object(DataChecker, "get_customer")
    @patch.object(DataChecker, "get_equipment")
    def test_customer_has_equipment_attached_valid_customer_valid_ptr_invalid_equipment(self, mocked_get_customer, mocked_get_equipment):
        # valid customer - valid equipment pointer
        self.dc.get_customer.return_value = [
            # customer
            [
                0, "", "", 0, "", "", "", "", "", None,
                0, # valid equipment pointer
                None, "", ""
            ]
        ]

        # invalid equipment
        self.dc.get_equipment.return_value = []

        assert self.dc.customer_has_equipment_attached(0) == False

    @patch.object(DataChecker, "get_customer")
    @patch.object(DataChecker, "get_equipment")
    def test_customer_has_equipment_attached_valid_all(self, mocked_get_customer, mocked_get_equipment):
        # valid customer - valid equipment pointer
        self.dc.get_customer.return_value = [
            # customer
            [
                0, "", "", 0, "", "", "", "", "", None,
                0, # valid equipment pointer
                None, "", ""
            ]
        ]

        # valid equipment
        self.dc.get_equipment.return_value = [
            # some equipment
            []
        ]

        assert self.dc.customer_has_equipment_attached(0) == True
