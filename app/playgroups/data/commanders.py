import json
import logging
import time
from collections import defaultdict
from typing import List

import requests

from playgroups.models import Commander
from playgroups.serializers import CommanderSerializer

logger = logging.getLogger("playgroups.data.commanders")

def SYNC_COMMANDER_DATA():
    service = CommanderDataService()
    service.sync_commander_data()


class CommanderDataService:
    fetch_endpoint = "https://api.scryfall.com/cards/search?q=is:commander%20-is:digital"
    headers={"Accept": "application/json", "User-Agent": "Arcanis/1.0"}

    def sync_commander_data(self):
        next_page = self.fetch_endpoint
        while next_page:
            json_data, next_page = self.fetch_commander_data(next_page)
            commander_dicts = self.transform_commander_data(json_data)
            self.save_commanders(commander_dicts)
            time.sleep(0.1)
        self.add_extra_commanders()

    def fetch_commander_data(self, url: str) -> tuple[List[dict], str | None]:
        logger.info("Fetching commander data")
        resp = requests.get(url, headers=self.headers)
        json_text = json.loads(resp.text)
        count = json_text.get("total_cards", 0)
        data = json_text.get("data")
        next_page = json_text.get("next_page")

        logger.info(f"Commander data fetched: {count} commanders found")
        if count == 0 or not data:
            raise Exception("No commander data found")
        
        return data, next_page


    def transform_commander_data(self, json_data) -> List[dict]:
        transformed_commanders = []
        for data in json_data:
            transformed = defaultdict(None)
            transformed["id"] = data["id"]
            transformed["name"] = data.get("name")
            if data.get("color_identity"):
                transformed["color_identity"] = "".join(data.get("color_identity"))
            else:
                transformed["color_identity"] = ""
            if data.get("image_uris") and data.get("image_uris").get("normal"):
                transformed["image"] = data.get("image_uris").get("normal")
            elif data.get("card_faces") and data.get("card_faces")[0].get("image_uris") and data.get("card_faces")[0].get("image_uris").get("normal"):
                transformed["image"] = data.get("card_faces")[0].get("image_uris").get("normal")
            transformed["scryfall_uri"] = data.get("scryfall_uri")
            
            transformed_commanders.append(transformed)
        return transformed_commanders


    def save_commanders(self, commander_dicts):
        create: List[dict] = []
        update: List[tuple] = []

        for commander_dict in commander_dicts:
            instance = Commander.objects.filter(pk=commander_dict["id"])
            if instance.count() == 0:
                create.append(commander_dict)
            elif instance.count() == 1:
                update.append((instance.get(), commander_dict))

        create_count = 0
        update_count = 0
        error_count = 0

        # create
        for create_data in create:
            serializer = CommanderSerializer(data=create_data)
            if serializer.is_valid(raise_exception=False):
                serializer.save(id=create_data["id"])
                create_count += 1
            else:
                logger.error(f"Error creating commander id={create_data["id"]}; invalid data")
                logger.error(serializer._errors)
                

                error_count += 1

        # update
        for (instance, update_data) in update:
            serializer = CommanderSerializer(instance, data=update_data, partial=False)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                update_count += 1
            else:
                logger.error(f"Error updating commander id={update_data["id"]}; invalid data")
                logger.error(serializer._errors)
                error_count += 1

        logger.info(f"Commanders created: {create_count}; updated: {update_count}; errors: {error_count}")


    def add_extra_commanders(self):
        witch = Commander(
            id="6914b30b-24f3-48cb-832f-c1f8510e2c9c", 
            name="Witch of the Moors", 
            color_identity="B", 
            image="https://cards.scryfall.io/normal/front/6/9/6914b30b-24f3-48cb-832f-c1f8510e2c9c.jpg?1712354364", 
            scryfall_uri="https://scryfall.com/card/otc/152/witch-of-the-moors?utm_source=api"
            )
        witch.save()
        
        tamanoa = Commander(
            id="6d32955b-cbf6-429b-9513-17ca75d4ec2c",
            name="Tamanoa",
            color_identity="GRW",
            image="https://cards.scryfall.io/normal/front/6/d/6d32955b-cbf6-429b-9513-17ca75d4ec2c.jpg?1593275551",
            scryfall_uri="https://scryfall.com/card/csp/132/tamanoa?utm_source=api"
        )
        tamanoa.save()

def print_ids():
    with open("playgroups/fixtures/commanders.json") as c, open("playgroups/fixtures/squirrels.json") as s:
        commanders = json.load(c)
        squirrels = json.load(s)

        commander_ids = [c["pk"] for c in commanders]
        match_players = [obj for obj in squirrels if obj.get("model") == "playgroups.matchplayer"]
        
        missing_ids = set()
        for mp in match_players:
            for id in mp["fields"]["commanders"]:
                if id not in commander_ids:
                    missing_ids.add(id)
        print(missing_ids)
        print(len(missing_ids))
    
