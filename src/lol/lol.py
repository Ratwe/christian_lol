from riotwatcher import LolWatcher, ApiError

from src.config import RIOT_API
from src.lol.calculating import calculate_participants_res

api_key = RIOT_API
watcher = LolWatcher(api_key)


def get_summoner_by_name(summoner_name: str, region: str):
    data = watcher.summoner.by_name(region, summoner_name)
    return data


def get_summoner_mastery(summoner_id: str, region: str):
    data = watcher.champion_mastery.by_summoner(region=region, encrypted_summoner_id=summoner_id)
    return data


def get_summoner_matches(summoner_puuid: str, region: str, limit: int):
    data = watcher.match.matchlist_by_puuid(region=region, puuid=summoner_puuid, count=limit)
    return data


def get_match_by_id(match_id: str, region: str):
    print(f"get_match: {match_id}, {region}")
    data = watcher.match.by_id(region, match_id)
    return data


def collect_participant_data(participant):
    keys = ["summonerName", "championName", "kills", "deaths", "assists"]

    participant_data = {}

    for key in keys:
        participant_data[key] = participant[key]

    return participant_data




def collect_match_info(match_id: str, region: str):
    data = get_match_by_id(match_id, region)
    info = data["info"]

    participants = info["participants"]
    gameMode = info["gameMode"]

    if gameMode != "CLASSIC":
        raise Exception("gameMode must be CLASSIC.")

    participants_data = []
    for participant in participants:
        participants_data.append(collect_participant_data(participant))

    return calculate_participants_res(participants_data)