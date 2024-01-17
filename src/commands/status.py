import logging
from discord.ext.commands import Bot, Context


async def cmd_status(bot: Bot, ctx: Context) -> None:
    if not bot.active:
        return
    
    # TODO:
    # running for X hours/days
    # number of spoiled cards in the last 24 hours/weeks

    await ctx.channel.send(
        "Hi! Mir geht's gut."
        )