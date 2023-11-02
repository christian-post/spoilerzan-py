import sys
import os
sys.path.append(os.getcwd())
import json
import logging
from typing import Union
from discord.ext.commands import Bot, Context

from src.utils import load_card_counts, load_sets, format_setnames


def remove_sets_from_files(
        setcodes: Union[str, list[str]], config: dict
    ) -> dict[str: list[str]]:
    
    sets_to_watch: list[str] = load_sets(config)
    card_counts: dict = load_card_counts(config)

    if type(setcodes) == str:
        setcodes = [setcodes,]

    sets_updated = {
        "success": set(),  # removed sets
        "failure": set()  # sets that could not be removed
    }
    
    for code in setcodes:
        set_to_remove = code.lower()

        failed = False

        try:
            sets_to_watch.remove(set_to_remove)
        except ValueError:
            sets_updated["failure"].add(set_to_remove)
            failed = True

        try:
            del card_counts[set_to_remove]
        except KeyError:
            sets_updated["failure"].add(set_to_remove)
            failed = True

        if failed:
            continue

        sets_updated["success"].add(set_to_remove)

    if len(sets_updated["success"]) > 0:
        with open(config["setsfile"], "w") as file:
            file.write(json.dumps(sets_to_watch))
        with open(config["cardcountsfile"], "w") as file:
            file.write(json.dumps(card_counts))
        
    return sets_updated




async def cmd_remove_set(bot: Bot, ctx: Context, *args: str) -> None:
    if not bot.active:
        return
    
    sets: list[str] = remove_sets_from_files(args, bot.config)
    if sets["success"]:
        await ctx.channel.send(
            f"Sets erfolgreich entfernt: {format_setnames(*sets['success'])}."
            )
    if sets["failure"]:
        await ctx.channel.send(
            f"Fehler beim Entfernen von: {format_setnames(*sets['failure'])}. Schreibe \"!spoilerzan sets\", um die Liste der Sets in der Datenbank einzusehen."
            )



if __name__ == "__main__":
    # TESTING
    import yaml

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    updated = remove_sets_from_files(["DMC", "NEC", "LTC"], config)
    logging.info(updated)