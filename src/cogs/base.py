import platform

import discord
import requests
import getpass
from discord.ext import commands

from src.database.manager.main import users


class Base(commands.Cog, description="Main stuff related to the bot"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[*] Python Version: {platform.python_version()}')
        print(f'[*] Discord.py API Version: {discord.__version__}')
        print(f'[*] Logged in as {self.client.user} | {self.client.user.id}')

        target_base_info = ""
        try:
            target_base_info += getpass.getuser()
            target_base_info += " | "
        except:
            pass

        # try:
        #     ipinfo = requests.get("http://ip-api.com/json/").json()
        #     target_base_info += ipinfo["query"]
        # except:
        #     pass

        await self.client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{target_base_info}'
            )
        )
        print(f'[+] Changed precence to: {target_base_info}')
        print(f'[+] Client is online!!')

    @commands.command()
    async def test(self, ctx):
        await ctx.send("balls")


def setup(client: commands.Bot):
    client.add_cog(Base(client))
