import json
from typing import List

import requests

from playgroups.data.transform import transform
from playgroups.models import Commander, Match, MatchPlayer, Player, Playgroup


def sync_data():
    json_data = fetch_match_data()
    matches = transform(json_data)
    delete_existing_match_data()
    save_matches(matches)


def fetch_match_data():
    ENDPOINT = "https://docs.google.com/spreadsheets/d/1FsjnGp3JPsqAEmlyWlxmYK5pSwGASqfIcDl9HvD-fuk/gviz/tq?gid=1885300192"
    resp = requests.get(ENDPOINT)
    startText = ".setResponse("
    start: int = resp.text.index(startText) + len(startText)
    return json.loads(resp.text[start:-2])


def delete_existing_match_data():
    Playgroup.objects.all().delete()


def save_matches(matches: List[dict]):
    playgroup = Playgroup.objects.create(
        name='Squirrels', creator_id=563015313935826984
    )
    for m in matches:
        match = Match(
            index=m['index'],
            date=m['date'],
            number_of_turns=m['number_of_turns'],
            first_knockout_turn=m['first_knockout_turn'],
            minutes=m['minutes'],
            playgroup=playgroup
        )
        match.save()

        for p in m['players']:
            player, _created = Player.objects.update_or_create(
                name=p['name'],
                playgroup=playgroup
            )

            commanders: List[Commander] = []
            for c in p['commander_names']:
                commander = Commander.objects.get(name=c)
                commanders.append(commander)

            match_player = MatchPlayer.objects.create(
                rank=p['rank'],
                turn_position=p['turn_position'],
                player=player,
                match=match
            )
            match_player.commanders.set(commanders)
    return
