# достать min/max данные из ParticipantDto по ключу key
def get_participant_info_by_key(participants, key: str, mode: str = "max"):
    if mode != "min":
        mode = "max"

    res_value = participants[0][key]
    res_participant = participants[0]

    for participant in participants:
        if mode == "min":
            if participant[key] < res_value:
                res_value = participant[key]
                res_participant = participant
        else:
            if participant[key] > res_value:
                res_value = participant[key]
                res_participant = participant

    return res_participant



def calculate_participants_res(participants):
    participants_res = {}

    keys = ["kills", "deaths", "assists"]
    modes = ["min", "max"]

    for key in keys:
        for mode in modes:
            participants_res[f"{mode}_{key}"] = get_participant_info_by_key(participants, key=key, mode=mode)["summonerName"]

    return participants_res
