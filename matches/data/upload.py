import json
from typing import List

import requests

from matches.data.transform import transform
from matches.models import Commander, Match, MatchPlayer


def sync_data():
    json_data = fetch_match_data()
    matches = transform(json_data)
    save_matches(matches)


def fetch_match_data():
    ENDPOINT = "https://docs.google.com/spreadsheets/d/1FsjnGp3JPsqAEmlyWlxmYK5pSwGASqfIcDl9HvD-fuk/gviz/tq?gid=1885300192"
    resp = requests.get(ENDPOINT)
    startText = ".setResponse("
    start: int = resp.text.index(startText) + len(startText)
    return json.loads(resp.text[start:-2])


def save_matches(matches: List[dict]):
    for m in matches:
        new_match = Match(
            index=m['index'],
            date=m['date'],
            number_of_turns=m['number_of_turns'],
            first_knockout_turn=m['first_knockout_turn'],
            minutes=m['minutes']
        )
        new_match.save()

        for p in m['players']:
            commanders: List[Commander] = []
            for c in p['commander_names']:
                commander = Commander.objects.get(name=c)
                commanders.append(commander)

            new_player = MatchPlayer.objects.create(
                name=p['name'],
                rank=p['rank'],
                turn_position=p['turn_position'],
                match=new_match
            )
            new_player.commanders.set(commanders)
    return
