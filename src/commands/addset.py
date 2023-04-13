import sys
import os
sys.path.append(os.getcwd())
import json

from src.utils import load_card_counts, load_sets, format_setnames


def add_sets_to_files(
        setcodes: str | list[str], config: dict
    ) -> dict[str: list[str]]:

    sets_to_watch: list[str] = load_sets(config)
    card_counts: dict = load_card_counts(config)

    if type(setcodes) == str:
        setcodes = [setcodes,]

    sets_updated = {
        "success": set(),  # newly added sets
        "contained": set(),  # sets that were already in the file
        "failure": set()  # sets that could not be added
    }
    
    for code in setcodes:
        set_to_add = code.lower()

        # TODO: check if set is valid?

        if set_to_add in sets_to_watch:
            sets_updated["contained"].add(set_to_add)
            continue

        sets_to_watch.append(set_to_add)
        card_counts[set_to_add] = { "card_count": 0 }

        sets_updated["success"].add(set_to_add)

    if len(sets_updated["success"]) > 0:
        with open(config["setsfile"], "w") as file:
            file.write(json.dumps(sets_to_watch))
        with open(config["cardcountsfile"], "w") as file:
            file.write(json.dumps(card_counts))
        
    return sets_updated


async def cmd_add_set(bot, ctx, *args):
    if not bot.active:
        return
    
    sets: list[str] = add_sets_to_files(args, bot.config)
    if sets["contained"]:
        await ctx.channel.send(
            f"Sets {format_setnames(*sets['contained'])} sind bereits in der Datenbank."
            )
    if sets["success"]:
        await ctx.channel.send(
            f"Sets erfolgreich hinzugefügt: {format_setnames(*sets['success'])}."
            )
    if sets["failure"]:
        await ctx.channel.send(
            f"Fehler beim Hinzufügen von: {format_setnames(*sets['failure'])}."
            )
    



if __name__ == "__main__":
    # TESTING
    import yaml

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    updated = add_sets_to_files(["DMC", "NEC", "LTC"], config)
    print(updated)