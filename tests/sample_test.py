import pytest

def case(x) :
    return str(x)

def test_test_case():
    assert case(5) == '5', f"expected string version of 5"