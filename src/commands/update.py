import sys
import os
sys.path.append(os.getcwd())

from src.utils import check_sets_for_spoilers, post_cards


async def cmd_update(bot, ctx, *args):
    # whether the cards should be posted to the channel, or just update
    should_post = "--np" not in args

    new_cards: list[dict] = check_sets_for_spoilers(bot.config)

    if new_cards:
        await ctx.channel.send(f"Update erfolgreich. {len(new_cards)} neue Spoiler vorhanden.")
        if should_post:
            channel = bot.get_channel(int(os.getenv("SPOILER_CHANNEL")))
            if not channel:
                print(f"No channel was found with the ID {os.getenv('SPOILER_CHANNEL')}")
            else:
                await post_cards(new_cards, channel)
    else:
        await ctx.channel.send("Keine neuen Spoiler in den zu beobachtenden Sets.")

