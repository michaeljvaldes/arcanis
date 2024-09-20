import datetime
from typing import List


def transform(data) -> List[dict]:
    matches = []
    for i, row in enumerate(data["table"]["rows"]):
        matches.append(row_to_match(row, i))

    # # for testing, just transform the first match and print it
    # matches.append(row_to_match(data['table']['rows'][0], 0))
    # print(matches)

    return matches


def row_to_match(row, index):
    match = {}
    match["index"] = index
    match["date"] = date_val(row["c"][2])
    match["number_of_turns"] = int_val(row["c"][19])
    match["first_knockout_turn"] = int_val(row["c"][20])
    match["minutes"] = int_val(row["c"][21])

    player1 = build_player(row["c"][3], row["c"][4], row["c"][5], row["c"][6])
    player2 = build_player(row["c"][7], row["c"][8], row["c"][9], row["c"][10])
    player3 = build_player(row["c"][11], row["c"][12], row["c"][13], row["c"][14])
    player4 = build_player(row["c"][15], row["c"][16], row["c"][17], row["c"][18])

    players = []

    # drop all empty players
    for player in [player1, player2, player3, player4]:
        if player["name"] is not None and player["name"] != "":
            players.append(player)

    players.sort(key=lambda p: int(p["turn_position"]))
    match["players"] = players

    return match


def build_player(name, commander_name, position, rank):
    player = {}
    player["name"] = str_val(name)
    commander_names = str_val(commander_name)
    if commander_names is not None:
        commander_names = commander_names.split(" && ")
    player["commander_names"] = commander_names
    player["turn_position"] = int_val(position)
    player["rank"] = int_val(rank)
    return player


def int_val(cell) -> int | None:
    if cell is None:
        return None
    return int(cell["v"])


def str_val(cell) -> str | None:
    if cell is None:
        return None
    return cell["v"]


def date_val(cell) -> datetime.date | None:
    if cell is None:
        return None
    date = cell["f"].split("/")
    return datetime.date(month=int(date[0]), day=int(date[1]), year=int(date[2]))
