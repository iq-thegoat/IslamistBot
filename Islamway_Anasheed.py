from islamway import Parser
import discord
from discord import app_commands
from discord.ext import commands
from Pagination import PaginatorViewNasheed, PaginatorView
from funks import create_embed
from islamway.Types import Nasheed
from icecream import ic
import textwrap

"""
    class PersistentViewBot(commands.Bot):
        def __init__(self):
            intents = discord.Intents().all()
            super().__init__(
                command_prefix=commands.when_mentioned_or("!"), intents=intents
            )

        async def setup_hook(self) -> None:
            self.add_view(PaginatorView())
            self.add_view(PaginatorViewNasheed())
"""


class Anasheed(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="search_nasheeds")
    @app_commands.describe(
        query="search query EX:name of the nasheed", limit="top %limit% nasheeds"
    )
    async def search_nasheeds(
        self, interaction: discord.Interaction, query: str, limit: int = 3
    ):
        parser = Parser()
        await interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.Anasheed.search_nasheed(query, limit)
            if results:
                for result in results:
                    try:
                        if result:
                            nasheed: Nasheed = result
                            embed = discord.Embed(
                                title=nasheed.name, colour=discord.Colour.light_embed()
                            )
                            embed.set_author(
                                name=nasheed.publisher,
                                url=nasheed.publisher_profile,
                                icon_url=nasheed.publisher_img,
                            )
                            print(nasheed.publisher_img)
                            embed.add_field(
                                name="summary", value=nasheed.text, inline=False
                            )
                            embed.add_field(
                                name="Views 👀", value=nasheed.views, inline=False
                            )
                            embed.add_field(
                                name="Likes ❤", value=nasheed.likes, inline=False
                            )
                            embed.add_field(
                                name="Dislikes 👎", value=nasheed.dislikes, inline=False
                            )
                            embed.add_field(
                                name="url", value=f"||{nasheed.nasheed_url}||"
                            )
                            embed.add_field(
                                name="Download link 📥",
                                value=f"||{nasheed.download_url}|| *press the download button*",
                            )
                            embed.add_field(
                                name="file_name", value=f"||{nasheed.filename}||"
                            )
                            embed.set_footer(
                                text=f"post date:{nasheed.publish_date.isoformat()}",
                                icon_url="data:image/jpeg;base64,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",
                            )

                    except Exception as e:
                        print(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service
                    try:
                        EMBEDS.append(embed)
                    except:
                        pass

                view = PaginatorViewNasheed(EMBEDS, interaction.user)
                await interaction.followup.send(embed=view.initial, view=view)
            else:
                await interaction.followup.send(
                    embed=await create_embed(
                        title="No Results",
                        content="No nasheeds found matching the query.",
                        color=discord.Colour.red(),
                    )
                )

        except Exception as e:
            print(e)
            await interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for nasheeds.",
                    color=discord.Colour.red(),
                )
            )

    @app_commands.command(name="most_popular_nasheeds")
    @app_commands.describe(limit="top %limit% nasheeds")
    async def most_popular_nasheeds(
        self, interaction: discord.Interaction, limit: int = 3
    ):
        parser = Parser()
        await interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.Anasheed.most_popular(limit=limit)
            if results:
                for result in results:
                    try:
                        if result:
                            nasheed: Nasheed = result
                            embed = discord.Embed(
                                title=nasheed.name, colour=discord.Colour.light_embed()
                            )
                            embed.set_author(
                                name=nasheed.publisher,
                                url=nasheed.publisher_profile,
                                icon_url=nasheed.publisher_img,
                            )
                            print(nasheed.publisher_img)
                            embed.add_field(
                                name="summary", value=nasheed.text, inline=False
                            )
                            embed.add_field(
                                name="Views 👀", value=nasheed.views, inline=False
                            )
                            embed.add_field(
                                name="Likes ❤", value=nasheed.likes, inline=False
                            )
                            embed.add_field(
                                name="dislikes 👎", value=nasheed.dislikes, inline=False
                            )
                            embed.add_field(
                                name="url", value=f"||{nasheed.nasheed_url}||"
                            )
                            embed.add_field(
                                name="download link 📥",
                                value=f"||{nasheed.download_url}|| *press the download button*",
                            )
                            embed.add_field(
                                name="file_name",
                                value=f"||{nasheed.filename.replace('*','')}||",
                            )
                            embed.set_footer(
                                text=f"post date:{nasheed.publish_date.isoformat()}",
                                icon_url="data:image/jpeg;base64,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",
                            )
                    except Exception as e:
                        print(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service
                    try:
                        EMBEDS.append(embed)
                    except:
                        pass

                view = PaginatorViewNasheed(EMBEDS, user=interaction.user)
                await interaction.followup.send(embed=view.initial, view=view)
            else:
                await interaction.followup.send(
                    embed=await create_embed(
                        title="No Results",
                        content="No nasheeds found matching the query.",
                        color=discord.Colour.red(),
                    )
                )

        except Exception as e:
            print(e)
            await interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for nasheeds.",
                    color=discord.Colour.red(),
                )
            )

    @app_commands.command(name="most_recent_nasheeds")
    @app_commands.describe(limit="top %limit% nasheeds")
    async def most_recent_nasheeds(
        self, interaction: discord.Interaction, limit: int = 3
    ):
        parser = Parser()
        await interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.Anasheed.most_recent(limit=limit)
            if results:
                for result in results:
                    try:
                        if result:
                            nasheed: Nasheed = result
                            embed = discord.Embed(
                                title=nasheed.name, colour=discord.Colour.light_embed()
                            )
                            embed.set_author(
                                name=nasheed.publisher,
                                url=nasheed.publisher_profile,
                                icon_url=nasheed.publisher_img,
                            )
                            print(nasheed.publisher_img)
                            embed.add_field(
                                name="summary", value=nasheed.text, inline=False
                            )
                            embed.add_field(
                                name="Views 👀", value=nasheed.views, inline=False
                            )
                            embed.add_field(
                                name="Likes ❤", value=nasheed.likes, inline=False
                            )
                            embed.add_field(
                                name="Dislikes 👎", value=nasheed.dislikes, inline=False
                            )
                            embed.add_field(
                                name="url", value=f"||{nasheed.nasheed_url}||"
                            )
                            embed.add_field(
                                name="Download link 📥",
                                value=f"||{nasheed.download_url}|| *press the download button*",
                            )
                            embed.add_field(
                                name="file_name", value=f"||{nasheed.filename}||"
                            )
                            embed.set_footer(
                                text=f"post date:{nasheed.publish_date.isoformat()}",
                                icon_url="data:image/jpeg;base64,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",
                            )
                    except Exception as e:
                        print(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service
                    try:
                        EMBEDS.append(embed)
                    except:
                        pass

                view = PaginatorViewNasheed(EMBEDS, interaction.user)
                await interaction.followup.send(embed=view.initial, view=view)
            else:
                await interaction.followup.send(
                    embed=await create_embed(
                        title="No Results",
                        content="No nasheeds found matching the query.",
                        color=discord.Colour.red(),
                    )
                )

        except Exception as e:
            print(e)
            await interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for nasheeds.",
                    color=discord.Colour.red(),
                )
            )

    @app_commands.command(name="most_viewed_nasheeds")
    @app_commands.describe(limit="top %limit% nasheeds")
    async def most_viewed_nasheeds(
        self, interaction: discord.Interaction, limit: int = 3
    ):
        parser = Parser()
        await interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.Anasheed.most_viewed()
            if results:
                for result in results:
                    try:
                        if result:
                            nasheed: Nasheed = result
                            embed = discord.Embed(
                                title=nasheed.name, colour=discord.Colour.light_embed()
                            )
                            embed.set_author(
                                name=nasheed.publisher,
                                url=nasheed.publisher_profile,
                                icon_url=nasheed.publisher_img,
                            )
                            print(nasheed.publisher_img)
                            embed.add_field(
                                name="summary", value=nasheed.text, inline=False
                            )
                            embed.add_field(
                                name="Views 👀", value=nasheed.views, inline=False
                            )
                            embed.add_field(
                                name="Likes ❤", value=nasheed.likes, inline=False
                            )
                            embed.add_field(
                                name="Dislikes 👎", value=nasheed.dislikes, inline=False
                            )
                            embed.add_field(
                                name="url", value=f"||{nasheed.nasheed_url}||"
                            )
                            embed.add_field(
                                name="Download link 📥",
                                value=f"||{nasheed.download_url}|| *press the download button*",
                            )
                            embed.add_field(
                                name="file_name", value=f"||{nasheed.filename}||"
                            )
                            embed.set_footer(
                                text=f"post date:{nasheed.publish_date.isoformat()}",
                                icon_url="data:image/jpeg;base64,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",
                            )
                    except Exception as e:
                        print(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service
                    try:
                        EMBEDS.append(embed)
                    except:
                        pass

                view = PaginatorViewNasheed(EMBEDS, interaction.user)
                await interaction.followup.send(embed=view.initial, view=view)
            else:
                await interaction.followup.send(
                    embed=await create_embed(
                        title="No Results",
                        content="No nasheeds found matching the query.",
                        color=discord.Colour.red(),
                    )
                )

        except Exception as e:
            print(e)
            await interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for nasheeds.",
                    color=discord.Colour.red(),
                )
            )


async def setup(bot):
    await bot.add_cog(Anasheed(bot=bot))
