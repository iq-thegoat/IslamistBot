import discord
from discord import app_commands
from discord.ext import commands
from dorrar import Parser, Types
from Pagination import PaginatorView
from funks import create_embed

class Dorrar(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="search_hadith")
    @app_commands.describe(
        query="search query EX:صوموا تصحوام",
        limit="top %limit% books",
        specialist="wether to search in specialist more complicated and long resources"
    )
    async def search_hadith(
        self,
        interaction: discord.Interaction,
        query: str,
        limit: int,
        specialist: bool
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
            results: list[Types.Hadith] = parser.search(query, limit=limit, specialist=specialist)
            MSGS = []

            for result in results:
                embed = discord.Embed()
                if embed is not None and result.text is not None:
                    embed.description = result.text.replace('REDALERTRIGHT', '__').replace('REDALERTLEFT', '__')
                else:
                     # Handle Discord API errors
                    await interaction.followup.send(embed=create_embed("Error","Erorr happened",discord.Color.red()))
                embed.add_field(name="الراوي", value=result.narrator,inline=True)
                embed.add_field(name="المحدث", value=result.muhadith,inline=True)
                embed.add_field(name="الحكم", value=result.ruling,inline=True)
                embed.add_field(name="المصدر", value=result.source,inline=True)
                embed.add_field(name="الصفحه او الرقم", value=result.page,inline=True)
                embed.add_field(name="رابط الحديث", value=result.url.replace('"',"").replace("'",""),inline=True)
                embed.add_field(name="شرح الحديث", value=result.sharh,inline=True)
                msg = f"> {result.text.replace('REDALERTRIGHT', '__').replace('REDALERTLEFT', '__')}"

                MSGS.append(embed)

            if len(MSGS) > 1:
                view = PaginatorView(MSGS)
                await interaction.followup.send(embed=view.initial, view=view)
            elif MSGS:
                await interaction.followup.send(MSGS[0][0], embed=MSGS[0][1])
            else:
                await interaction.followup.send(embed=create_embed("NO RESULTS 😔😔","No results found.",discord.Color.red()))

        except (discord.errors.HTTPException, discord.errors.NotFound) as e:
            # Handle Discord API errors
            await interaction.followup.send(embed=create_embed("Error",e,discord.Color.red()))

async def setup(bot):
    await bot.add_cog(Dorrar(bot=bot))
