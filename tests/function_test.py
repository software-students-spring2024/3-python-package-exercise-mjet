import pytest
import os
import requests
import sys
sys.path.insert(0,'../src/pyFilmFinder')
from finder import Finder
finder = Finder()
print("all ok")
API_KEY = os.getenv('API_KEY')
finder.api_key = API_KEY
def test_api_key():
    print(API_KEY)
    assert len(API_KEY) == 32, f"incorrect length for api key"
    assert finder.validate_api_key(), f"api key not valid tests won't pass"  