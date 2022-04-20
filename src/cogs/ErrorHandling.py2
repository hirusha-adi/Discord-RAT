import discord
from discord.ext import commands
from datetime import datetime


class ErrorHandling(commands.Cog, description="Handle the errors raised by the bot"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        embed = discord.Embed(
            title="An error has occured",
            color=0xff0000,
            timestamp=datetime.utcnow()
        )
        embed.set_author(
            name=str(self.client.user.name),
            icon_url=str(self.client.user.avatar_url)
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
                value=f"Bot Missing Role. {self.client.user.name} does not have any role for this.",
                inline=False
            )

        if isinstance(error, commands.BotMissingPermissions):
            embed.add_field(
                name="Error:",
                value=f"Bot Missing Permissions. {self.client.user.name} does not have enough permission for this command to be run successfully.",
                inline=False
            )

        if isinstance(error, commands.BotMissingRole):
            embed.add_field(
                name="Error:",
                value=f"Bot Missing Role. {self.client.user.name} does not have a required role to complete this action.",
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


def setup(client: commands.Bot):
    client.add_cog(ErrorHandling(client))
