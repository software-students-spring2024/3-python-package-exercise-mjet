import os
import requests
from dotenv import load_dotenv


class FilmFinder:
    """
    A utility class for fetching information about films from The Movie Database (TMDb) API.
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

    def search_films(self, keyword: str) -> str:
        """
        Searches for films based on a specified keyword.

        Read More:
            https://developer.themoviedb.org/reference/search-movie
        View Sample JSON Response:
            https://api.themoviedb.org/3/search/movie?language=en-US&page=1&query=cars&api_key={self.api_key}
        """
        api_url = f"https://api.themoviedb.org/3/search/movie?language=en-US&page=1&query={keyword}&api_key={self.api_key}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            films = response.json()
            # TODO: parse results, return n number of films
            return films.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return []

    def find_films(self, genres: str = None, cast: str = None, year: int = None) -> str:
        """
        Fetches a list of films based on specified genres, cast, and release year.

        Read More:
            https://developer.themoviedb.org/reference/discover-movie
        View Sample JSON Response:
            - Genres 12 OR 14
            "https://api.themoviedb.org/3/discover/movie?language=en-US&with_genres=12%2C14&api_key={self.api_key}"
            - Genres 12 AND 14
            "https://api.themoviedb.org/3/discover/movie?language=en-US&with_genres=12%7C14&api_key={self.api_key}"
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

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            films = response.json()
            # TODO: parse results, return n number of films
            return films.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return []

    def find_similar(self, film_id: int) -> str:
        """
        Fetches a list of movies similar to the specified movie.

        Read More:
            https://developer.themoviedb.org/reference/movie-recommendations
        View Sample JSON Response:
            https://api.themoviedb.org/3/movie/920/recommendations?api_key={self.api_key}
        """
        api_url = (
            f"{self.base_url}movie/{film_id}/recommendations?api_key={self.api_key}"
        )

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            films = response.json()
            # TODO: parse results, return n number of films
            return films.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return []

    def get_details(self, film_id: int) -> str:
        """
        Read More:
            https://developer.themoviedb.org/reference/movie-details
        View Sample JSON Response:
            https://api.themoviedb.org/3/movie/920?language=en-US&api_key={self.api_key}
            - Appended Credits includes
            https://api.themoviedb.org/3/movie/550?language=en-US&append_to_response=credits&api_key={self.api_key}
        """
        api_url = (
            f"{self.base_url}movie/{film_id}?language=en-US&api_key={self.api_key}"
        )

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            details = response.json()
            # TODO: parse response for desired fields (view sample JSON !)
            return details.get("original_title", [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return []
