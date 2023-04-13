import time
import requests
import json
from typing import Any



def load_sets(config: dict) -> list[str]:
    try:
        with open(config["setsfile"], "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"The file {config['setsfile']} appears corrupted. Loading empty set list.")
        return []
    except FileNotFoundError as err:
        print(err)
        return []
    

def load_card_counts(config: dict) -> dict[str: dict[str: int]]:
    """
    example output: {"unf":{"card_count":638},"clb":{"card_count":327}}
    """
    try:
        with open(config["cardcountsfile"], "r") as file:
            return json.load(file)
    except FileNotFoundError as err:
        print(err)
        return {}


def get_set_data(setcode: str, config: dict) -> dict:
    """
    Gets the set data for the given set code from the scryfall API
    """
    # reduce number of requests
    time.sleep(config["sleeptime"])

    res = requests.get(config["urlsets"] + setcode)
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        print(f"The set \"{setcode}\" could not be accessed. Error code {res.status_code}.\n")
        return {}


def get_spoiled_cards(set_data: dict, config: dict) -> list:
    """
    fetches spoiled cards for the given set
    returns a list with the card objects
    """
    cards = []

    url = config["urlspoiledcards"] + set_data.get("code", "")
    if config["verbose"]:
        print(f"Looking for spoilers at {url}\n")
    res = requests.get(url)
    if res.status_code == 200:
        card_data = json.loads(res.text)
        cards += card_data.get("data")
        next_page = card_data.get("next_page")

        # load cards as long as the data points to a next page
        if card_data.get("has_more"):
            while True:
                if config["verbose"]:
                    print(f"More cards at {next_page}\n")
                time.sleep(config["sleeptime"])

                res = requests.get(next_page)
                if res.status_code != 200:
                    break
                more_card_data = json.loads(res.text)
                cards += more_card_data.get("data")
                if not more_card_data.get("has_more"):
                    break
                next_page = more_card_data.get("next_page")

    else:
        print(f"Error fetching cards for \"{set_data['code']}\" at {url}. Error code {res.status_code}.\n")

    return cards


def check_sets_for_spoilers(config: dict) -> list[Any]:
    """
    for each set in the setsfile, send a request for spoiled cards.
    if the number of cards is greater than in the cardcountsfile,
        cards are added to the returned list and the cardcountsfile is 
        updated
    returns: List of card objects
    """
    sets: list[str] = load_sets(config)
    card_counts: dict = load_card_counts(config)

    if not (sets and card_counts):
        print("There is something wrong with the set data or card counts data.")
        return []
    
    # Flag will be set to true if card counts changed
    counts_need_update = False

    new_cards = []
    for set_ in sets:
        set_data = get_set_data(set_, config)

        if not set_data:
            continue

        # check if the card count is the same as in the data
        new_count = set_data.get("card_count", 0)
        old_count = card_counts.get(
            set_data.get("code"), {}
            ).get("card_count", 0)
        
        if config["verbose"]:
            print(f"Set \"{set_data.get('name')} ({set_})\", new card count: {new_count}, old card count: {old_count}.\n")

        # new cards have been spoiled since last time
        if new_count > old_count:
            num_spoiled = new_count - old_count

            cards = get_spoiled_cards(set_data, config)
            if not cards:
                continue

            new_cards += cards[:num_spoiled]

            # update the card count in server data
            card_counts[set_]["card_count"] = new_count
            counts_need_update = True

    if counts_need_update:
        # update the server file
        with open(config["cardcountsfile"], "w") as file:
            file.write(json.dumps(card_counts))

    return new_cards


def format_card_data_for_post(card_data: dict) -> str:
    # Check if card is DFC
    if card_data.get("layout") == "transform":
        front_face = card_data.get("card_faces", [])[0]
        back_face = card_data.get("card_faces", [])[1]

        post_string = f"""{card_data.get("scryfall_uri")}

{card_data.get("name")}
{front_face.get("name")} {front_face.get("mana_cost")}
{front_face.get("type_line")}
{front_face.get("oracle_text")}
//
{back_face.get("name")}
{back_face.get("type_line")}
{back_face.get("oracle_text")}

{front_face.get("image_uris", {}).get("normal")}
{back_face.get("image_uris", {}).get("normal")}
"""
    else:
        post_string = f"""{card_data.get("scryfall_uri")}

{card_data.get("name")} {card_data.get("mana_cost")}
{card_data.get("type_line")}
{card_data.get("oracle_text")}
{card_data.get("image_uris", {}).get("normal")}
"""

    return post_string


def format_setnames(*setnames: list[str]) -> str:
    uppercase_names = list(map(lambda x: f'\"{x.upper()}\"', setnames))
    return ', '.join(uppercase_names)


async def post_cards(cardlist: list[dict], channel) -> None:
    for i, card in enumerate(cardlist):
        time.sleep(0.2)
        print(i, card.get("name"))
        await channel.send(format_card_data_for_post(card))



if __name__ == "__main__":
    # TESTS

    # from dotenv import load_dotenv
    # import sys
    # import os
    # sys.path.append(os.getcwd())

    # import yaml

    # with open('config.yaml', 'r') as file:
    #     config = yaml.safe_load(file)

    # # set that doesn't exist
    # get_set_data("FOO", config)

    # # set that exists
    # mom_data = get_set_data("MOM", config)
    # print("Data for MOM:", mom_data)

    # mom_cards = get_spoiled_cards(mom_data, config)
    # print(format_card_data_for_post(mom_cards[0]))
    # print(format_card_data_for_post(mom_cards[1]))
    # print(format_card_data_for_post(mom_cards[2]))
    # print(format_card_data_for_post(mom_cards[3]))


    setnames = set(["foo", "bar", "baz"])
    print(format_setnames(*setnames))