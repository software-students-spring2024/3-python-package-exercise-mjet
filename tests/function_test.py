import pytest
import os
import requests
import sys
from src.pyFilmFinder.finder import Finder
finder = Finder()
API_KEY = os.getenv('API_KEY')
finder.api_key = API_KEY
def test_api_key():
    print(API_KEY)
    assert len(API_KEY) == 32, f"incorrect length for api key"
    assert finder.validate_api_key(), f"api key not valid tests won't pass"  
def test_get_films_fail():
    api_url = "ntesterrornothinghere"
    outputtemp = finder.get_films(api_url)
    assert outputtemp[:31] == "Failed to fetch films from API:", f"error anticipated"
    #tests behavior for api failing

def test_get_films_success():
    api_url = f"https://api.themoviedb.org/3/discover/movie?language=en-US&api_key={API_KEY}"
    outputtemp = finder.get_films(api_url)
    assert "Failed to fetch" not in outputtemp, f"failed to fetch"

def test_find_films():
    api_url = f"https://api.themoviedb.org/3/discover/movie?language=en-US&api_key={API_KEY}"
    outputtemp2 = finder.get_films(api_url)
    outputtemp = "Title:KungFuPanda4Released:2024-03-02(ID:1011985)VoteAverage:6.927Description:PoisgearinguptobecomethespiritualleaderofhisValleyofPeace,butalsoneedssomeonetotakehisplaceasDragonWarrior.Assuch,hewilltrainanewkungfupractitionerforthespotandwillencounteravillaincalledtheChameleonwhoconjuresvillainsfromthepast.Title:RoadHouseReleased:2024-03-08(ID:359410)VoteAverage:7.3Description:Ex-UFCfighterDaltontakesajobasabouncerataFloridaKeysroadhouse,onlytodiscoverthatthisparadiseisnotallitseems.Title:GodzillaxKong:TheNewEmpireReleased:2024-03-27(ID:823464)VoteAverage:7.404Description:Followingtheirexplosiveshowdown,GodzillaandKongmustreuniteagainstacolossalundiscoveredthreathiddenwithinourworld,challengingtheirveryexistence-andourown.WatchHere:https://ln.run/2CILgTitle:MadameWebReleased:2024-02-14(ID:634492)VoteAverage:5.633Description:Forcedtoconfrontrevelationsaboutherpast,paramedicCassandraWebbforgesarelationshipwiththreeyoungwomendestinedforpowerfulfutures...iftheycanallsurviveadeadlypresent.Title:AlienoidReleased:2022-07-20(ID:601796)VoteAverage:7.2Description:Intheyear2022,aRobotGuardmanagesalienprisonerstrappedinsidehumanbrains.RaisingtheyounggirlEanonEarth,helivesintheguiseofahumanbeing.Oneday,whenanalienprisonerescapes,theentireplanetisthrownintojeopardyandGuardgoesbacktothepastwithEantotrapthealienthere.Meanwhile630yearsearlierduringtheGoryeoDynasty,anolderEanisknownasTheGirlWhoShootsThunder.WhileEanistryingtoretrievetheDivineBlade,thekeytotravelingthroughtime,Muruk,ahaplessdosa(Koreantaomagician),isaimingtoclaimtheenormousbountyplacedonit."
    assert outputtemp.strip().replace(" ", "")[:50] == finder.find_films().strip().replace(" ","")[:50], f"incorrect output for find"
    #the result is subject to change this test probably needs revision
    assert outputtemp2 == finder.find_films(), f"incorrect output for find films w api call"
    #this result depends on the api call
    #TODO add result for incorrect parameters

def test_search_films():
    api_url = f"https://api.themoviedb.org/3/search/movie?language=en-US&page=1&query=iron&api_key={API_KEY}"
    outputtemp = finder.get_films(api_url)
    assert outputtemp == finder.search_films("iron"), f"incorrect output for search"
    outputtemp2 ="Title:DetectiveConan:BlackIronSubmarineReleased:2023-04-14(ID:1047041)VoteAverage:6.8Description:ManyengineersfromaroundtheworldgatherattheInterpolmarinefacility"
    assert outputtemp2.strip().replace(" ", "")[:50] == finder.search_films("iron").strip().replace(" ", "")[:50], f"incorrect output for search"

def test_get_details():
    fail_url = "nothing here"
    failresponse = finder.get_details(fail_url)
    assert failresponse[:31] == "Failed to fetch films from API:", f"error anticipated"
    #TODO parser not implemented so not tested for this part

def test_find_similar():
    api_url = f"https://api.themoviedb.org/3/movie/27205/recommendations?api_key={API_KEY}"
    outputtemp = finder.get_films(api_url)
    assert outputtemp == finder.find_similar(27205)
    outputtemp2 = "Title:TheDarkKnightReleased:2008-07-16(ID:155)VoteAverage:8.515Description:Batmanraisesthestakesinhiswaroncrime.WiththehelpofLt.JimGordonandDistrictAttorneyHarveyDent,Batmansetsouttodismantletheremainingcriminalorganizationsthatplaguethestreets.Thepartnershipprovestobeeffective,buttheysoonfindthemselvespreytoareignofchaosunleashedbyarisingcriminalmastermindknowntotheterrifiedcitizensofGothamastheJoker.Title:InterstellarReleased:2014-11-05(ID:157336)VoteAverage:8.431Description:Theadventuresofagroupofexplorerswhomakeuseofanewlydiscoveredwormholetosurpassthelimitationsonhumanspacetravelandconquerthevastdistancesinvolvedinaninterstellarvoyage.Title:ShutterIslandReleased:2010-02-14(ID:11324)VoteAverage:8.202Description:WorldWarIIsoldier-turned-U.S.MarshalTeddyDanielsinvestigatesthedisappearanceofapatientfromahospitalforthecriminallyinsane,buthiseffortsarecompromisedbytroublingvisionsandamysteriousdoctor.Title:AvatarReleased:2009-12-15(ID:19995)VoteAverage:7.58Description:Inthe22ndcentury,aparaplegicMarineisdispatchedtothemoonPandoraonauniquemission,butbecomestornbetweenfollowingordersandprotectinganaliencivilization.Title:TheHungerGamesReleased:2012-03-12(ID:70160)VoteAverage:7.205Description:EveryyearintheruinsofwhatwasonceNorthAmerica,thenationofPanemforceseachofitstwelvedistrictstosendateenageboyandgirltocompeteintheHungerGames.Parttwistedentertainment,partgovernmentintimidationtactic,theHungerGamesareanationallytelevisedeventinwhich“Tributes”mustfightwithoneanotheruntilonesurvivorremains.Pittedagainsthighly-trainedTributeswhohavepreparedfortheseGamestheirentirelives,KatnissisforcedtorelyuponhersharpinstinctsaswellasthementorshipofdrunkenformervictorHaymitchAbernathy.Ifshe’severtoreturnhometoDistrict12,Katnissmustmakeimpossiblechoicesinthearenathatweighsurvivalagainsthumanityandlifeagainstlove.Theworldwillbewatching."
    assert outputtemp2.strip().replace(" ", "")[:50] == finder.find_similar(27205).strip().replace(" ", "")[:50], f"incorrect output for similar"