import pytest
import os
import requests
import sys
import finder
import json
import find_similar

finder = finder.Finder()

target_film_id  = finder.get_film_id('Die Hard')
target_film_dict = finder.get_film_dict(target_film_id)

similarity = finder.rank_similar_by_overview(finder.get_film_id('Die Hard'))

print(similarity)


with open('tests/get_id_diehard.json', 'w') as f:
    json.dump(target_film_id, f)

with open('tests/get_dict_diehard.json', 'w') as f: 
    json.dump(target_film_dict, f)

with open('tests/rank_similar_diehard.json', 'w') as f:
    json.dump(similarity, f)

with open('tests/get_id_diehard.json') as f:
    solution = json.load(f)
