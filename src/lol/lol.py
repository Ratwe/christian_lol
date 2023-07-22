from riotwatcher import LolWatcher, ApiError

from src.auth.utils import get_user_db

talon_id = 91
api_key = 'RGAPI-0f4602e9-ca51-40ba-a8cd-99352e98cfa8'
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


def get_match_info(match_id: str, region: str):
    data = watcher.match.by_id(region, match_id)
    return data

def load_match_info(match_data):
    user_db = get_user_db()