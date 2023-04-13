import sys
import os
sys.path.append(os.getcwd())

from src.utils import load_sets, get_set_data, format_setnames


async def cmd_sets(bot, ctx, *args):
    if not bot.active:
        return
    
    await ctx.channel.send("Einen Moment bitte...")
    
    sets_to_watch = load_sets(bot.config)

    if sets_to_watch:
        out_string = "Sets unter Beobachtung:"
    else:
        out_string = "Keine Sets unter Beobachtung."
    
    for setcode in sets_to_watch:
        set_data = get_set_data(setcode, bot.config)

        if not set_data:
            name = f"{format_setnames(setcode)} (Unknown Set)"
            uri = "---"
        else:
            name = set_data.get('name')
            uri = f"{set_data.get('scryfall_uri')}?order=spoiled"

        out_string += f"\n• {name}\n{uri}"

    message = await ctx.channel.send(out_string)
    # remove URL embeds
    await message.edit(suppress=True)

