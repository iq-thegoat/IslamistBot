from islamway import Parser
import discord
from discord import app_commands
from discord.ext import commands
from Pagination import BooksPaginator  # going to use this cause of the download button
from funks import create_embed
from islamway.Types import Book
from icecream import ic


class Books(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="islamway_search_books")
    @app_commands.describe(
        query="search query EX:name of the book", limit="top %limit% books"
    )
    async def islamway_search_books(
        self, interaction: discord.Interaction, query: str, limit: int = 3
    ):
        parser = Parser()
        await interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.Books.search_book(query, limit)
            if results:
                for result in results:
                    try:
                        if result:
                            book: Book = result
                            embed = discord.Embed(
                                title=book.name, color=discord.Colour.lighter_grey()
                            )
                            embed.set_author(
                                name=book.publisher_name,
                                url=book.publisher_url,
                                icon_url=book.publisher_img,
                            )
                            embed.description = (
                                book.text
                            )  # Use the property instead of the method
                            embed.add_field(
                                name="Views 👀", value=book.views, inline=False
                            )
                            embed.add_field(
                                name="Likes ❤", value=book.likes, inline=False
                            )
                            embed.add_field(
                                name="Dislikes 👎", value=book.dislikes, inline=False
                            )
                            embed.add_field(name="url", value=f"||{book.url}||")
                            embed.add_field(
                                name="Download link 📥",
                                value=f"||{book.download_link}|| *press the download button*",
                            )
                            embed.add_field(
                                name="file_name", value=f"||{book.filename}||"
                            )
                            embed.set_image(url=book.img)

                    except Exception as e:
                        ic(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service

                    try:
                        EMBEDS.append(embed)
                    except:
                        pass
                view = BooksPaginator(EMBEDS, interaction.user)
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
            ic(e)
            await interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for nasheeds.",
                    color=discord.Colour.red(),
                )
            )


async def setup(bot):
    await bot.add_cog(Books(bot=bot))
