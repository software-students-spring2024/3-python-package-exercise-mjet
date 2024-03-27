import pytest
import os

def test_api_key():
    API_KEY = os.getenv('API_KEY')
    print(API_KEY)
    assert len(API_KEY) == 32, f"incorrect length for api key"
