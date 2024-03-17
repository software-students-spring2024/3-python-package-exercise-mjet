import os
import argparse  # https://docs.python.org/3/library/argparse.html
from dotenv import load_dotenv
from filmFinder import FilmFinder


def main():
    """
    Entry point for the Film Finder CLI application.
    """
    finder = FilmFinder()
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        while True:
            api_key = input("Enter your API key: ")
            finder.api_key = api_key
            if finder.validate_api_key():
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"API_KEY={finder.api_key}\n")
                break
            print("Invalid API key. Please provide a valid API key.")

    parser = argparse.ArgumentParser(description="Film Finder CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command to search films
    search_parser = subparsers.add_parser(
        "search",
        help="Search for films by keywords",
        description="Search for films based on a keyword. Usage: pyFilmFinder search <keyword>",
    )
    search_parser.add_argument("keyword", help="Keyword to search for")

    # Command to find films
    find_parser = subparsers.add_parser(
        "find",
        help="Find films by genres, cast, and optionally a release year",
        description="Find films based on specified genres, cast, and optionally a release year.\n"
        "Usage: pyFilmFinder find [--genres GENRES] [--cast CAST] [--year YEAR]",
    )
    # TODO: allow multiple genres
    find_parser.add_argument("--genres", default=None, help="Genres to filter by")
    # TODO: allow multiple cast memebers (directors and actors)
    find_parser.add_argument("--cast", default=None, help="Cast to filter by")
    # TODO: allow user to input decade in place of year
    find_parser.add_argument("--year", default=None, help="Year to filter by")

    # Command to find similar films
    similar_parser = subparsers.add_parser(
        "similar",
        help="Find films similar to the specified film",
        description="Find films that are similar to a specified film. Usage: pyFilmFinder similar --id FILM_ID",
    )
    similar_parser.add_argument("--id", help="Film ID to find similar films for")

    args = parser.parse_args()

    # TODO: print help if no arguments are provided

    # TODO: replace print statement based what each function returns
    if args.command == "search":
        finder.search_films(args.keyword)
        print("search films")
    elif args.command == "find":
        finder.find_films(args.genres, args.cast, args.year)
        print("find films")
    elif args.command == "similar":
        finder.find_similar(args.id)
        print("find similar")


if __name__ == "__main__":
    main()
