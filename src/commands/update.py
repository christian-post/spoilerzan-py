import sys
import os
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
import logging

from src.utils import check_sets_for_spoilers, post_cards


async def update_helper(bot, should_post=True):
    new_cards: list[dict] = check_sets_for_spoilers(bot.config)

    if new_cards and should_post:
        channel = bot.get_channel(int(os.getenv("SPOILER_CHANNEL")))
        if not channel:
            logging.warning(f"No channel was found with the ID {os.getenv('SPOILER_CHANNEL')}")
        else:
            await post_cards(new_cards, channel)

    return new_cards


async def cmd_update(bot, ctx, *args):
    interval = datetime.now() - bot.last_updated
    if interval < timedelta(seconds=bot.config["updatespaminterval_s"]):
        await ctx.channel.send("Die Datenbank wurde vor kurzem geupdated.")
        return
    bot.last_updated = datetime.now()
    # whether the cards should be posted to the channel, or just update
    should_post = "--np" not in args

    new_cards = await update_helper(bot, should_post)

    if new_cards:
        await ctx.channel.send(f"Update erfolgreich. {len(new_cards)} neue Spoiler vorhanden.")
    else:
        await ctx.channel.send("Keine neuen Spoiler in den zu beobachtenden Sets.")

