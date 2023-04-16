from datetime import datetime
from dotenv import load_dotenv
from discord.ext import tasks
from discord.ext.commands import Context, errors

from bot import Spoilerzan
from commands import descriptions
from commands.addset import cmd_add_set
from commands.removeset import cmd_remove_set
from commands.sets import cmd_sets
from commands.update import cmd_update, update_helper



if __name__ == "__main__":
    load_dotenv()

    bot = Spoilerzan()

    # --- configure commands and tasks --- #

    # @bot.command(name="help", description=descriptions.get("help"))
    # async def help_me(ctx: Context) -> None:
    #     helptext = ""
    #     for command in bot.commands:
    #         helptext += f"{command}\n"
    #     await ctx.channel.send(helptext)


    @bot.command(name="addSet", description=descriptions.get("addSet"))
    async def add_set(ctx, *args) -> None:
        """
        Add one or multiple sets to the sets-to-watch file
        example: !spoilerzan addSet MAT MUL MOM
        """
        await cmd_add_set(bot, ctx, *args)


    @bot.command(name="removeSet", description=descriptions.get("removeSet"))
    async def remove_set(ctx: Context, *args: str) -> None:
        """
        Remove one or multiple sets from the sets-to-watch file
        example: !spoilerzan removeSet MAT MUL MOM
        """
        await cmd_remove_set(bot, ctx, *args)


    @bot.command(name="sets", description=descriptions.get("sets"))
    async def sets(ctx: Context, *args: str) -> None:
        """
        List all Sets that are being watched
        """
        await cmd_sets(bot, ctx, *args)


    @bot.command(name="update", description=descriptions.get("update"))
    async def update(ctx: Context, *args: str) -> None:
        """
        Updates the card count database and posts the new cards
        suppress posting with --np argument
        """
        await cmd_update(bot, ctx, *args)


    @tasks.loop(minutes=int(bot.config["updateinterval_min"]))
    async def update_loop() -> None:
        """
        Periodically looks for new spoilers and posts them to Discord
        """
        print(f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} Looking for new spoilers...")
        new_cards = await update_helper(bot, should_post=True)
        print(f"{len(new_cards)} cards were spoiled and posted to the channel.\n")


    @bot.event
    async def on_ready() -> None:
        print(f"We have logged in as {bot.user}")

        # start the periodic update
        update_loop.start()


    @bot.event
    async def on_message_error(ctx, error):
        if isinstance(error, errors.CommandNotFound):
            await ctx.channel.send("Unbekannter Befehl.")
            # await help_me(ctx)


    # connect the Bot to Discord
    bot.run()