import os

import discord
from discord.ext import commands

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

if __name__ == "__main__":
    client.run(db_main.token)
