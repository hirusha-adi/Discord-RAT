import platform

import discord
from discord.ext import commands

from bot.database.manager.main import users


class Base(commands.Cog, description="Main stuff related to the bot"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[*] Python Version: {platform.python_version()}')
        print(f'[*] Discord.py API Version: {discord.__version__}')
        print(f'[*] Logged in as {self.client.user} | {self.client.user.id}')

        await self.client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{len(self.client.guilds)} servers!'
            )
        )
        print(f'[*] Client is online!!')


def setup(client: commands.Bot):
    client.add_cog(Base(client))
