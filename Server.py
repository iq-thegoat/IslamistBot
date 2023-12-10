import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from Noor_Wrapper import Parser, Types
from funks import create_embed, config
from typing import Optional


class Server(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="search_in_server")
    @app_commands.describe(
        query="search query EX: name of the book",
        msgcap="how many messages to check in each channel, default=250",
        channel="if you want to search in a specific channel",
    )
    async def search_in_server(
        self,
        Interaction: discord.Interaction,
        query: str,
        msgcap: int = 250,
        channel: Optional[discord.TextChannel] = None,
    ):
        await Interaction.response.defer()
        try:
            if channel:
                messages = channel.history(limit=msgcap)
                async for msg in messages:
                    if query.lower() in msg.content.lower():
                        await Interaction.followup.send(
                            msg.content + "\n" + msg.jump_url
                        )
                        return

            else:
                for channel in self.bot.get_all_channels():
                    if isinstance(channel, discord.CategoryChannel) or isinstance(
                        channel, discord.ForumChannel
                    ):
                        pass
                    else:
                        if channel:
                            messages = channel.history(limit=msgcap)
                            async for msg in messages:
                                if query.lower() in msg.content.lower():
                                    await Interaction.followup.send(
                                        msg.content + "\n" + msg.jump_url
                                    )
                                    return

            await Interaction.followup.send(
                embed=await create_embed(
                    title="No Results",
                    content="No matching messages found in the specified channel(s).",
                    color=discord.Colour.red(),
                )
            )

        except Exception as e:
            print(
                e
            )  # Log the error, you can modify this to log to a file or a logging service
            await Interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching in the server.",
                    color=discord.Colour.red(),
                )
            )


async def setup(bot):
    await bot.add_cog(Server(bot=bot))
