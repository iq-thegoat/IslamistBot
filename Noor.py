import discord
from discord import app_commands
from discord.ext import commands
from Noor_Wrapper import Parser, Types
from Pagination import PaginatorView
from funks import create_embed


class Noor(commands.Cog):
    def __init__(self, bot: discord.Client):
        """
        Initializes the Noor cog.

        Parameters:
        - bot (discord.Client): The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="noor_search")
    @app_commands.describe(
        query="search query EX:name of the book", limit="top %limit% books"
    )
    async def noor_search(
        self, Interaction: discord.Interaction, query: str, limit: int = 1
    ):
        """
        Searches for books and sends the results as embeds.

        Parameters:
        - Interaction (discord.Interaction): The Discord interaction.
        - query (str): The search query.
        - limit (int, optional): The number of top books to display. Defaults to 1.
        """
        parser = Parser()
        await Interaction.response.defer()
        EMBEDS = []
        try:
            results = parser.search(query, limit=limit)
            if results:
                top_results = results[0:limit]
                for book in top_results:
                    book: Types.SearchResult = book
                    try:
                        if book:
                            book: Types.Book = parser.parse_book_page(book.url)
                            print(book.model_dump_json(indent=3))
                            # print(book)
                            embed = discord.Embed(
                                title=book.title, colour=discord.Colour.light_embed()
                            )
                            embed.add_field(
                                name="Author", value=book.author, inline=False
                            )
                            embed.add_field(
                                name="Language", value=book.language, inline=False
                            )
                            embed.add_field(
                                name="Number Of Pages",
                                value=book.pages_count,
                                inline=False,
                            )
                            embed.add_field(
                                name="category", value=book.category, inline=False
                            )
                            embed.add_field(name="Download:", value=book.URL)
                            if book.img_url:
                                embed.set_image(url=book.img_url)
                    except Exception as e:
                        print(
                            e
                        )  # Log the error, you can modify this to log to a file or a logging service
                    try:
                        EMBEDS.append(embed)
                    except:
                        pass
                if len(EMBEDS) > 1:
                    view = PaginatorView(EMBEDS,Interaction.user)
                    await Interaction.followup.send(embed=view.initial, view=view)
                else:
                    await Interaction.followup.send(embed=EMBEDS[0])
            else:
                await Interaction.followup.send(
                    embed=await create_embed(
                        title="No Results",
                        content="No books found matching the query.",
                        color=discord.Colour.red(),
                    )
                )
        except Exception as e:
            print(e)
            await Interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while searching for books.",
                    color=discord.Colour.red(),
                )
            )

    @app_commands.command(name="parse_book")
    @app_commands.describe(noor_book_url="URL for the book from the noor-book.com site")
    async def send_in_embed(self, Interaction: discord.Interaction, noor_book_url: str):
        """
        Parses a book page and sends book details as an embed.

        Parameters:
        - Interaction (discord.Interaction): The Discord interaction.
        - noor_book_url (str): The URL of the book page on noor-book.com.
        """
        parser = Parser()
        await Interaction.response.defer()
        try:
            book = parser.parse_book_page(noor_book_url)
            if book:
                embed = discord.Embed(
                    title=book.title, colour=discord.Colour.light_embed()
                )
                embed.add_field(name="Author", value=book.author, inline=False)
                embed.add_field(name="Language", value=book.language, inline=False)
                embed.add_field(
                    name="Number Of Pages", value=book.pages_count, inline=False
                )
                embed.add_field(name="Publisher", value=book.publisher, inline=False)
                embed.add_field(name="Download:", value=book.shortened_url)
                if book.img_url:
                    embed.set_image(url=book.img_url)
                await Interaction.followup.send(embed=embed)
            else:
                await Interaction.followup.send(
                    embed=await create_embed(
                        title="Book Not Found",
                        content="The specified book was not found.",
                        color=discord.Colour.red(),
                    )
                )
        except Exception as e:
            print(e)
            await Interaction.followup.send(
                embed=await create_embed(
                    title="Oops",
                    content="An error occurred while parsing the book.",
                    color=discord.Colour.red(),
                )
            )


async def setup(bot):
    """
    Asynchronously adds the Noor cog to the bot.

    Parameters:
    - bot: The Discord bot instance.
    """
    await bot.add_cog(Noor(bot=bot))
