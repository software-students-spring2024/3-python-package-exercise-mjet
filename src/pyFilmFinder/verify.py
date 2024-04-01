import pytest
import os
import requests
import sys
import finder
import find_similar

finder = finder.Finder()

target_film  = finder.get_film_id('Die Hard')
similarity = finder.rank_similar_by_overview(target_film)
print(similarity)
