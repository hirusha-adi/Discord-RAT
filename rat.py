import os

import discord
from discord.ext import commands

from src.database.manager import main as db_main

client = commands.Bot(command_prefix=db_main.prefix)

# Load all cogs at startup of the bot
for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'bot.cogs.{filename[:-3]}')
            print(f"[+] Loaded: bot.cogs.{filename[:-3]}")
        except Exception as excl:
            print(
                f"[+] Unable to load: bot.cogs.{filename[:-3]}  :  {excl}")


@client.command()
async def loadex(ctx, extension):
    client.load_extension(
        f'bot.cogs.{extension if not(str(extension).endswith(".py")) else extension[:-3]}')
    await ctx.send(f"Loaded cog: {extension}")


@client.command()
async def unloadex(ctx, extension):
    client.unload_extension(
        f'bot.cogs.{extension if not(str(extension).endswith(".py")) else extension[:-3]}')
    await ctx.send(f"Un-Loaded cog: {extension}")


if __name__ == "__main__":
    client.run(db_main.token)
