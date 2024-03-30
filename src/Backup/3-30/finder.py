import os
import requests
from dotenv import load_dotenv
import find_similar

class Finder:
    """
    A utility class for fetching information about films from The Movie Database (TMDB) API.
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://api.themoviedb.org/3/"

    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request to the API endpoint.
        """
        api_url = f"{self.base_url}authentication?api_key={self.api_key}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return False

    def find_films(self, genres: str = None, cast: str = None, year: int = None) -> str:
        """
        Fetches a list of films based on specified genres, cast, and release year.
        """
        # TODO: convert incoming genre(s) to their corresponding id(s)
        # genres_id = {
        #     "action": 28,
        #     "adventure": 12,
        #     "animation": 16,
        #     "comedy": 35,
        #     "documentary": 99,
        #     "drama": 18,
        #     "family": 10751,
        #     "fantasy": 14,
        #     "history": 36,
        #     "horror": 27,
        #     "music": 10402,
        #     "mystery": 9648,
        #     "romance": 10749,
        #     "science-fiction": 878,
        #     "thriller": 53,
        #     "tv-movie": 10770,
        #     "war": 10752,
        #     "western": 37,
        # }
        api_url = f"{self.base_url}discover/movie?language=en-US&api_key={self.api_key}"

        # TODO: validate params
        if genres:
            api_url += f"&with_genres={genres}"
        if cast:
            api_url += f"&with_cast={cast}"
        if year:
            api_url += f"&primary_release_year={year}"

        return self.get_films(api_url)

    def search_films(self, keyword: str) -> str:
        """
        Searches for films based on a specified keyword.
        """
        api_url = f"{self.base_url}search/movie?language=en-US&page=1&query={keyword}&api_key={self.api_key}"
        return self.get_films(api_url)

    def find_similar(self, film_id: int) -> str:
        """
        Fetches a list of movies similar to the specified movie.
        """
        api_url = (
            f"{self.base_url}movie/{film_id}/recommendations?api_key={self.api_key}"
        )
        return self.get_films(api_url)
    
    #return a ranking of films sorted by similar sounding overviews
    def rank_similar_by_overview(self, film_id: int) -> str:

        """
        target_film  = finder.get_film_dict(finder.get_film_id('cloverfield'))
        overview = target_film['overview']
        genres = [genre['name'] for genre in target_film['genres']]
        """

        target_film = self.get_film_dict(film_id)
        #get films in same genre
        api_url = f"{self.base_url}discover/movie?language=en-US&api_key={self.api_key}"
        films_in_genre = self.get_films_nostr(api_url)
        for film in films_in_genre:
            if not type(film) == dict:
                films_in_genre.remove(film) 

        if target_film not in films_in_genre:
            films_in_genre += [target_film]

        return find_similar.tf_idf(target_film, films_in_genre)

    def get_details(self, film_id: int) -> str:
        """
        Fetches detailed information about the specified film.
        """
        api_url = (
            f"{self.base_url}movie/{film_id}?language=en-US&api_key={self.api_key}"
        )
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            details = response.json()
            # TODO: parse response for desired fields
            return details
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch films from API: {e}."

    def format_film(self, film: dict) -> str:
        """
        Format the given film information into a readable string.
        """
        title = film.get("title", "")
        film_id = film.get("id", "")
        vote_average = film.get("vote_average", "")
        overview = film.get("overview", "")

        formatted_film = (
            f"Title: {title} (ID: {film_id}) Vote Average: {vote_average}\n"
        )
        formatted_film += f"Description: {overview}\n\n"
        return formatted_film
    
    #return id of the first film appearing in a search for a given kword
    def get_film_id(self, keyword: str) -> int:
        api_url = f"{self.base_url}search/movie?language=en-US&page=1&query={keyword}&api_key={self.api_key}"
        response = requests.get(api_url, timeout = 10)
        films = response.json().get('results',[])
        if len(films) == 0:
            print("No results found")
            return -1
        else:
            return films[1]['id']

    #return the dict object associated with a given film id
    def get_film_dict(self, film_id: int) -> dict:
        #api_url = f"{self.base_url}movie/{film_id}/?api_key={self.api_key}"
        api_url = f"{self.base_url}movie/{film_id}?language=en-US&api_key={self.api_key}"
        response = requests.get(api_url, timeout = 10)
        films = response.json()
        return films
    
    #return the results of a given request without converting it into a string
    def get_films_nostr(self, api_url):
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        films = response.json()
        if films.get("total_results", 0) == 0:
            return "No results found."
        films = films.get("results", [])
        return films

    def get_films(self, api_url: str) -> str:
        """
        Retrieve films from the specified API URL and return them as a formatted string.
        """
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            films = response.json()
            if films.get("total_results", 0) == 0:
                return "No results found."
            films = films.get("results", [])
            formatted_films = ""
            count = 0
            for film in films:
                if count >= 5:
                    break
                if (
                    not film.get("title")
                    or not film.get("vote_average")
                    or not film.get("overview")
                    or film.get("popularity", 0) < 10
                ):
                    continue
                formatted_films += self.format_film(film)
                count += 1
            return formatted_films
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch films from API: {e}."
