import pytest
import os
import requests
from finder import Finder
API_KEY = os.getenv('API_KEY')
def validate_api_key(API_KEY) -> bool:
        """
        Validate the API key by making a test request to the API endpoint.
        """
        api_url = f"https://api.themoviedb.org/3/authentication?api_key={API_KEY}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return False
def test_api_key():
    print(API_KEY)
    assert len(API_KEY) == 32, f"incorrect length for api key"
    assert validate_api_key(API_KEY), f"api key not valid tests won't pass"    