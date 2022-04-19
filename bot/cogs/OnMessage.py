import discord
from discord.ext import commands

from bot.database.manager import blacklisted
from bot.database.manager import main


class OnMessage(commands.Cog, description="Handle the messages sent"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, message: discord.Message):

        """
        The bot can only be used by `users` and in `channel_ids` only!
        If another user tried to send a message with this bot's prefix
            The bot will reply with a saying the bot is still under development
        """

        if self.client.user == message.author:
            return

        if message.content.lower().startswith(main.prefix):
            await message.reply("This bot is still under development. Stay tuned! Thank you.")

        if not (message.channel.id in main.channel_ids):
            return

        if not (message.author.id in main.users):
            return

        if self.client.user.mentioned_in(message):
            await message.reply(f'Hey, My bot prefix is {main.prefix}')

        await self.client.process_commands(message)


def setup(client: commands.Bot):
    client.add_cog(OnMessage(client))
