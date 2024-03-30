import pytest
import os
import requests
import sys
import finder
import find_similar

finder = finder.Finder()

target_film  = finder.get_film_dict(finder.get_film_id('cloverfield'))
finder.rank_similar_by_overview(target_film)
