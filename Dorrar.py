import discord
from discord import app_commands
from discord.ext import commands
from dorrar import Parser, Types
from Pagination import PaginatorView
from funks import create_embed
import textwrap
from icecream import ic
from copy import deepcopy


class Dorrar(commands.Cog):
    """
    A Discord cog for searching and displaying Hadiths.

    Attributes:
        bot (discord.Client): The Discord bot instance.
    """

    def __init__(self, bot: discord.Client):
        """
        Initialize the Dorrar cog.

        Args:
            bot (discord.Client): The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="search_hadith")
    @app_commands.describe(
        query="search query EX:صوموا تصحوام",
        limit="top %limit% books",
        specialist="wether to search in specialist more complicated and long resources",
    )
    async def search_hadith(
        self, interaction: discord.Interaction, query: str, limit: int, specialist: bool
    ):
        """
        Search for Hadiths based on the provided query.

        Args:
            interaction (discord.Interaction): The interaction object.
            query (str): The search query.
            limit (int): The limit of top books.
            specialist (bool): Whether to search in specialist resources.

        Raises:
            discord.errors.HTTPException: If there is an issue with Discord API requests.
            discord.errors.NotFound: If the requested resource is not found.
        """
        try:
            await interaction.response.defer()
            parser = Parser()
            results: list[Types.Hadith] = parser.search(
                query, limit=limit, specialist=specialist
            )
            MSGS = []

            for result in results:
                embed = discord.Embed()
                if embed is not None and result.text is not None:
                    MSG = result.text.replace("REDALERTRIGHT", "").replace(
                        "REDALERTLEFT", ""
                    )
                    msgs = textwrap.wrap(MSG, 2034, break_long_words=True)

                else:
                    # Handle Discord API errors
                    await interaction.followup.send(
                        embed=await create_embed(
                            "Error", "Error happened", discord.Color.red()
                        )
                    )

                embed.add_field(name="الراوي", value=result.narrator, inline=True)
                embed.add_field(name="المحدث", value=result.muhadith, inline=True)
                embed.add_field(name="الحكم", value=result.ruling, inline=True)
                embed.add_field(name="المصدر", value=result.source, inline=True)
                embed.add_field(name="الصفحه او الرقم", value=result.page, inline=True)
                embed.add_field(
                    name="رابط الحديث",
                    value=result.url.replace('"', "").replace("'", ""),
                    inline=True,
                )
                embed.add_field(name="شرح الحديث", value=result.sharh, inline=True)

                for msg in msgs:
                    d = deepcopy(embed)
                    d.description = "```" + msg + "```"
                    MSGS.append(d)

            if len(MSGS) > 1:
                view = PaginatorView(MSGS, user=interaction.user)
                await interaction.followup.send(embed=view.initial, view=view)
            elif MSGS:
                await interaction.followup.send(embed=MSGS[0]) # sending the only embed in the list in case there is only one result
            else:
                await interaction.followup.send(
                    embed=await create_embed(
                        "NO RESULTS 😔😔", "No results found.", discord.Color.red()
                    )
                )

        except (discord.errors.HTTPException, discord.errors.NotFound) as e:
            # Handle Discord API errors
            await interaction.followup.send(
                embed=await create_embed("Error", e, discord.Color.red())
            )


async def setup(bot):
    """
    Setup function for adding the Dorrar cog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.

    Returns:
        None
    """
    await bot.add_cog(Dorrar(bot=bot))
