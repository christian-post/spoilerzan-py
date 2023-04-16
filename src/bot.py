import os
import sys
sys.path.append(os.getcwd())
from datetime import datetime
import yaml

import discord
from discord.ext import commands




class Spoilerzan(commands.Bot):
    def __init__(self):
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix="!spoilerzan ", intents=intents)
        self._token: str = os.getenv("CLIENT_TOKEN")

        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.active = True
        self.last_updated = datetime.now()


    def run(self):
        super().run(self._token)




    