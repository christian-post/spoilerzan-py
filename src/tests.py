import sys
import os
sys.path.append(os.getcwd())
import json
import yaml
from typing import Any

from utils import (
    check_sets_for_spoilers, 
    load_card_counts,
    format_card_data_for_post
)
from commands.addset import add_sets_to_files


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


# set the card count manually for testing
add_sets_to_files("mom", config)

card_counts = load_card_counts(config)
card_counts["mom"] = { "card_count": 380 }

with open(config["cardcountsfile"], "w") as file:
    file.write(json.dumps(card_counts))

new_cards: list[Any] = check_sets_for_spoilers(config)
print(len(new_cards), "new cards spoiled.\n")

if new_cards:
    for card in new_cards:
        print(card)
        print(format_card_data_for_post(card))