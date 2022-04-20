import discord
from discord.ext import commands

from src.database.manager import main


class OnMessage(commands.Cog, description="Handle the messages sent"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        """
        The bot can only be used by `users` and in `channel_ids` only!
        If another user tried to send a message with this bot's prefix
            The bot will reply with a saying the bot is still under development
        """

        # bot self check
        if self.client.user == message.author:
            return

        # Send bot prefix
        if self.client.user.mentioned_in(message):
            await message.reply(f'Hey, My bot prefix is {main.prefix}')


def setup(client: commands.Bot):
    client.add_cog(OnMessage(client))
