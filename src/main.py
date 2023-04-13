from dotenv import load_dotenv

from bot import Spoilerzan
from commands.addset import cmd_add_set
from commands.removeset import cmd_remove_set
from commands.sets import cmd_sets
from commands.update import cmd_update


if __name__ == "__main__":
    load_dotenv()

    bot = Spoilerzan()

    @bot.command(name="hello")
    async def greet(ctx):
        await ctx.channel.send(f"Hi there, {ctx.message.author}")

    @bot.command(name="addSet")
    async def add_set(ctx, *args):
        """
        Add one or multiple sets to the sets-to-watch file
        example: !spoilerzan addSet MAT MUL MOM
        """
        await cmd_add_set(bot, ctx, *args)

    @bot.command(name="removeSet")
    async def remove_set(ctx, *args):
        """
        Remove one or multiple sets from the sets-to-watch file
        example: !spoilerzan removeSet MAT MUL MOM
        """
        await cmd_remove_set(bot, ctx, *args)

    @bot.command(name="sets")
    async def sets(ctx, *args):
        """
        List all Sets that are being watched
        """
        await cmd_sets(bot, ctx, *args)

    @bot.command(name="update")
    async def update(ctx, *args):
        """
        Updates the card count database and posts the new cards
        suppress posting with --np argument
        """
        await cmd_update(bot, ctx, *args)

    bot.run()