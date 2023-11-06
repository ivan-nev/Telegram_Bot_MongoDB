from app import check_data
from data_test import qw1, qw2, qw3, ans1, ans2, ans3
from app import error_format


def test_check_data():
    assert check_data(qw1) == ans1
    assert check_data(qw2) == ans2
    assert check_data(qw3) == ans3


def test_error_data():
    assert check_data({'data_from': 'sdf'}) == error_format()
