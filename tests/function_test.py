import pytest
import os
import requests
import sys
import json
from src.pyFilmFinder.finder import Finder

finder = Finder()
API_KEY = os.getenv("API_KEY")
finder.api_key = API_KEY


def test_api_key():
    print(API_KEY)
    assert len(API_KEY) == 32, f"incorrect length for api key"
    assert finder.validate_api_key(), f"api key not valid tests won't pass"


def test_get_films_fail():
    api_url = "ntesterrornothinghere"
    outputtemp = finder.get_films(api_url)
    assert outputtemp[:31] == "Failed to fetch films from API:", f"error anticipated"
    # tests behavior for api failing


def test_get_films_success():
    api_url = (
        f"https://api.themoviedb.org/3/discover/movie?language=en-US&api_key={API_KEY}"
    )
    outputtemp = finder.get_films(api_url)
    assert "Failed to fetch" not in outputtemp, f"failed to fetch"


def test_find_films():
    api_url = (
        f"https://api.themoviedb.org/3/discover/movie?language=en-US&api_key={API_KEY}"
    )
    outputtemp2 = finder.get_films(api_url)
    outputtemp = 'Title: Godzilla x Kong: The New Empire Released: 2024-03-27 (ID: 823464) Vote Average: 7.092\nDescription: Following their explosive showdown, Godzilla and Kong must reunite against a colossal undiscovered threat hidden within our world, challenging their very existence – and our own.\n\nTitle: Kung Fu Panda 4 Released: 2024-03-02 (ID: 1011985) Vote Average: 6.923\nDescription: Po is gearing up to become the spiritual leader of his Valley of Peace, but also needs someone to take his place as Dragon Warrior. As such, he will train a new kung fu practitioner for the spot and will encounter a villain called the Chameleon who conjures villains from the past.\n\nTitle: Road House Released: 2024-03-08 (ID: 359410) Vote Average: 7.278\nDescription: Ex-UFC fighter Dalton takes a job as a bouncer at a Florida Keys roadhouse, only to discover that this paradise is not all it seems.\n\nTitle: Madame Web Released: 2024-02-14 (ID: 634492) Vote Average: 5.648\nDescription: Forced to confront revelations about her past, paramedic Cassandra Webb forges a relationship with three young women destined for powerful futures...if they can all survive a deadly present.\n\nTitle: Creation of the Gods I: Kingdom of Storms Released: 2023-07-20 (ID: 856289) Vote Average: 7.195\nDescription: Based on the most well-known classical fantasy novel of China, Fengshenyanyi, the trilogy is a magnificent eastern high fantasy epic that recreates the prolonged mythical wars between humans, immortals and monsters, which happened more than three thousand years ago.\n\n'
    assert (
        outputtemp.strip().replace(" ", "")[:50]
        == finder.find_films().strip().replace(" ", "")[:50]
    ), f"incorrect output for find"
    # the result is subject to change this test probably needs revision
    assert (
        outputtemp2 == finder.find_films()
    ), f"incorrect output for find films w api call"
    # this result depends on the api call
    # TODO add result for incorrect parameters


def test_search_films():
    api_url = f"https://api.themoviedb.org/3/search/movie?language=en-US&page=1&query=iron&api_key={API_KEY}"
    outputtemp = finder.get_films(api_url)
    assert outputtemp == finder.search_films("iron"), f"incorrect output for search"
    outputtemp2 = 'Title: Kabaneri of the Iron Fortress Recap 2: Burning Life Released: 2017-01-07 (ID: 431803) Vote Average: 8.2\nDescription: Compilation film of the second half of the TV series.\n\nTitle: Detective Conan: Black Iron Submarine Released: 2023-04-14 (ID: 1047041) Vote Average: 6.8\nDescription: Many engineers from around the world gather at the Interpol marine facility "Pacific Buoy" on Hachijo-jima, in the sea south of central Tokyo Prefecture coast, to witness the launch of a new system that connects all law enforcement camera systems around the world and enables facial recognition worldwide. Conan, along with his friends Kogoro, Ran, Agasa, Haibara, and the Detective Boys, also heads to the island with an invitation from Sonoko to see the whales. He receives a message from Subaru, who says that a Europol agent has been murdered in Germany by Gin. Perturbed, Conan sneaks onto the police ship led by Kuroda, which is bringing them to the island to protect the completion work, and tours the new facility, just in time for the Black Organization to kidnap a female engineer, seeking a piece of important data in her USB drive. A terrifying howl of screws is heard from the ocean as an unknown person approaches Haibara.\n\nTitle: The Iron Claw Released: 2023-12-21 (ID: 850165) Vote Average: 7.58\nDescription: The true story of the inseparable Von Erich brothers, who made history in the intensely competitive world of professional wrestling in the early 1980s. Through tragedy and triumph, under the shadow of their domineering father and coach, the brothers seek larger-than-life immortality on the biggest stage in sports.\n\nTitle: Iron Man: Rise of Technovore Released: 2013-04-24 (ID: 169934) Vote Average: 6.0\nDescription: Iron Man enlists the help of ruthless vigilante the Punisher to track down War Machine\'s murderer. All the while, he\'s being pursued by S.H.I.E.L.D. agents Black Widow and Hawkeye, who suspect his involvement in a recent terrorist plot.\n\nTitle: Iron Will Released: 1994-01-14 (ID: 24767) Vote Average: 6.6\nDescription: When Will Stoneman\'s father dies, he is left alone to take care of his mother and their land. Needing money to maintain it, he decides to join a cross country dogsled race. This race will require days of racing for long hours, through harsh weather and terrain. This young man will need a lot of courage and a strong will to complete this race.\n\n'
    assert (
        outputtemp2.strip().replace(" ", "")[:50]
        == finder.search_films("iron").strip().replace(" ", "")[:50]
    ), f"incorrect output for search"


def test_get_details_fails():
    fail_url = "nothing here"
    failresponse = finder.get_details(fail_url)
    assert failresponse[:31] == "Failed to fetch films from API:", f"error anticipated"
    # TODO parser not implemented so not tested for this part


# working here johan
def test_get_details():
    film_id = 13
    api_url = (
        f"https://api.themoviedb.org/3/movie/{film_id}?language=en-US&api_key={API_KEY}"
    )
    output = ""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        details = response.json()
        # TODO: parse response for desired fields
        title = details.get("title", "")
        film_id = details.get("id", "")
        vote_average = details.get("vote_average", "")
        overview = details.get("overview", "")
        release_date = details.get("release_date", "")
        tagline = details.get("tagline", "")
        released = details.get("status", "")
        budget = details.get("budget", "")
        popularity = details.get("popularity", "")
        revenue = details.get("revenue", "")
        genre_names = [genre["name"] for genre in details["genres"]]
        production_companies = [
            company["name"] for company in details["production_companies"]
        ]

        details_formatted = "======================================================================================"
        details_formatted += f"\nTitle: {title}\nReleased: {release_date}\n(ID: {film_id})\nGenres: {genre_names}\nProduction Companies: {production_companies}\nStatus: {released}\nBudget: {budget}\nVote Average: {vote_average}\nPopularity Score: {popularity}\nRevenue: {revenue}\n"
        details_formatted += f"Description: {overview}\nTagline: {tagline}\n\n"
        details_formatted += "======================================================================================"
        output = details_formatted

    except requests.exceptions.RequestException as e:
        return f"Failed to fetch films from API: {e}."

    assert output == finder.get_details(13), f"incorrect output for search"


def test_find_similar():
    api_url = (
        f"https://api.themoviedb.org/3/movie/27205/recommendations?api_key={API_KEY}"
    )
    outputtemp = finder.get_films(api_url)
    assert outputtemp == finder.find_similar(27205)
    outputtemp2 = "Title:TheDarkKnightReleased:2008-07-16(ID:155)VoteAverage:8.515Description:Batmanraisesthestakesinhiswaroncrime.WiththehelpofLt.JimGordonandDistrictAttorneyHarveyDent,Batmansetsouttodismantletheremainingcriminalorganizationsthatplaguethestreets.Thepartnershipprovestobeeffective,buttheysoonfindthemselvespreytoareignofchaosunleashedbyarisingcriminalmastermindknowntotheterrifiedcitizensofGothamastheJoker.Title:InterstellarReleased:2014-11-05(ID:157336)VoteAverage:8.431Description:Theadventuresofagroupofexplorerswhomakeuseofanewlydiscoveredwormholetosurpassthelimitationsonhumanspacetravelandconquerthevastdistancesinvolvedinaninterstellarvoyage.Title:ShutterIslandReleased:2010-02-14(ID:11324)VoteAverage:8.202Description:WorldWarIIsoldier-turned-U.S.MarshalTeddyDanielsinvestigatesthedisappearanceofapatientfromahospitalforthecriminallyinsane,buthiseffortsarecompromisedbytroublingvisionsandamysteriousdoctor.Title:AvatarReleased:2009-12-15(ID:19995)VoteAverage:7.58Description:Inthe22ndcentury,aparaplegicMarineisdispatchedtothemoonPandoraonauniquemission,butbecomestornbetweenfollowingordersandprotectinganaliencivilization.Title:TheHungerGamesReleased:2012-03-12(ID:70160)VoteAverage:7.205Description:EveryyearintheruinsofwhatwasonceNorthAmerica,thenationofPanemforceseachofitstwelvedistrictstosendateenageboyandgirltocompeteintheHungerGames.Parttwistedentertainment,partgovernmentintimidationtactic,theHungerGamesareanationallytelevisedeventinwhich“Tributes”mustfightwithoneanotheruntilonesurvivorremains.Pittedagainsthighly-trainedTributeswhohavepreparedfortheseGamestheirentirelives,KatnissisforcedtorelyuponhersharpinstinctsaswellasthementorshipofdrunkenformervictorHaymitchAbernathy.Ifshe’severtoreturnhometoDistrict12,Katnissmustmakeimpossiblechoicesinthearenathatweighsurvivalagainsthumanityandlifeagainstlove.Theworldwillbewatching."
    assert (
        outputtemp2.strip().replace(" ", "")[:50]
        == finder.find_similar(27205).strip().replace(" ", "")[:50]
    ), f"incorrect output for similar"


def test_format_film():
    film = {
        "title": "Ratatouille",
        "id": "2062",
        "vote_average": "7.818",
        "overview": "Remy, a resident of Paris, appreciates good food and has quite a sophisticated palate. He would love to become a chef so he can create and enjoy culinary masterpieces to his heart's delight. The only problem is, Remy is a rat. When he winds up in the sewer beneath one of Paris' finest restaurants, the rodent gourmet finds himself ideally placed to realize his dream.",
        "release_date": "2007-06-28",
    }
    title = film.get("title", "")
    film_id = film.get("id", "")
    vote_average = film.get("vote_average", "")
    overview = film.get("overview", "")
    release_date = film.get("release_date", "")
    test_formatted_film = f"Title: {title} Released: {release_date} (ID: {film_id}) Vote Average: {vote_average}\n"
    test_formatted_film += f"Description: {overview}\n\n"

    assert test_formatted_film == finder.format_film(film)

def test_rank_similar_by_overview():
    with open('tests/rank_similar_diehard.json') as f:
        solution = json.load(f)
    assert solution == finder.rank_similar_by_overview(finder.get_film_id('Die Hard'))

def test_get_film_id():
    with open('tests/get_id_diehard.json') as f:
        solution = json.load(f)
    assert solution == finder.get_film_id('Die Hard')

def test_get_film_dict():
    with open('tests/get_dict_diehard.json') as f:
        solution = json.load(f)
    assert solution == finder.get_film_dict(finder.get_film_id('Die Hard'))


