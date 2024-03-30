from finder import Finder

finder = Finder()
#finder.search_films("cloverfield")


film  = finder.get_film_dict(finder.get_film_id('cloverfield'))
overview = film['overview']
pass
