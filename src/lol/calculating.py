def get_min_kills(participants):
    min_kills = participants[0]["kills"]
    participant_min_kills = participants[0]

    for participant in participants:
        if participant["kills"] < min_kills:
            min_kills = participant["kills"]
            participant_min_kills = participant

    return participant_min_kills


def get_max_deaths(participants):
    max_deaths = participants[0]["deaths"]
    participant_max_deaths = participants[0]

    for participant in participants:
        if participant["deaths"] > max_deaths:
            max_deaths = participant["deaths"]
            participant_max_deaths = participant

    return participant_max_deaths


def get_min_assists(participants):
    min_assists = participants[0]["assists"]
    participant_min_assists = participants[0]

    for participant in participants:
        if participant["assists"] < min_assists:
            min_assists = participant["assists"]
            participant_min_assists = participant

    return participant_min_assists


def calculate_participants_res(participants):
    participants_res = {}

    participant_min_kills = get_min_kills(participants)
    participants_res[str(participant_min_kills["summoner_name"]): "он вообще не убивал"]

    participant_max_deaths = get_max_deaths(participants)
    participants_res[str(participant_max_deaths["summoner_name"]): "дох как муха"]

    participant_min_assists = get_min_assists(participants)
    participants_res[str(participant_min_assists["summoner_name"]): "стилер килов"]

    return participants_res
