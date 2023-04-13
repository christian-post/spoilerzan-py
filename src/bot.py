import os
import sys
sys.path.append(os.getcwd())
import json
import yaml

import discord
from discord.ext import commands




class Spoilerzan(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix="!spoilerzan ", intents=intents)
        self._token = os.getenv("CLIENT_TOKEN")

        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.active = True


    def run(self):
        super().run(self._token)


    async def on_ready(self):
        print(f"We have logged in as {self.user}")




    