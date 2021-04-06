from datachecker import DataChecker

class TestDataChecker:
    pass

    def test_check_valid_age(self):
        dc = DataChecker()

        assert dc.check_valid_age(1) == True
        assert dc.check_valid_age(-1) == False
        assert dc.check_valid_age(1.5) == False
        assert dc.check_valid_age("one") == False
