import discord
from typing import List
from collections import deque
from discord.ext import commands
from discord.ui import View, Button
import aiohttp
from funks import *
import io
from icecream import ic
class PaginatorView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]):
        """
        A paginator view for displaying a list of embeds.

        Args:
            embeds (List[discord.Embed]): List of embeds to paginate.
        """
        super().__init__(timeout=None)
        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self._queue[0].set_footer(text=f"Pages Of {self._current_page}/{self._len}")

    async def update_buttons(self, interaction: discord.Interaction):
        """
        Update the pagination buttons based on the current state.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        for i in self._queue:
            i.set_footer(text=f"Pages Of {self._current_page}/{self._len}")
        if self._current_page == self._len:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        if self._current_page == 1:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        await interaction.message.edit(view=self)

    @discord.ui.button(emoji="👈")
    async def previous(self, interaction: discord.Interaction, _):
        """
        Move to the previous page.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.defer()
        self._queue.rotate(-1)
        embed = self._queue[0]
        self._current_page -= 1
        await self.update_buttons(interaction)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(emoji="👉")
    async def next(self, interaction: discord.Interaction, _):
        """
        Move to the next page.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        self._queue.rotate(1)
        embed = self._queue[0]
        self._current_page += 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    @property
    def initial(self) -> discord.Embed:
        """
        Get the initial embed.

        Returns:
            discord.Embed: The initial embed.
        """
        return self._initial

'''
class StrPaginatorView(discord.ui.View):
    def __init__(self, MSGS: List[tuple]):
        """
        A paginator view for displaying a list of strings and embeds.

        Args:
            MSGS (List[tuple]): List of tuples containing a string and an embed.
        """
        super().__init__(timeout=None)
        self._embeds = MSGS
        self._queue = deque(MSGS)
        self._initial = MSGS[0]
        self._len = len(MSGS)
        self._current_page = 1
        self.children[0].disabled = True
        self._queue[0][1].set_footer(text=f"Pages Of {self._current_page}/{self._len}")

    async def update_buttons(self, interaction: discord.Interaction):
        """
        Update the pagination buttons based on the current state.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        for i in self._queue:
            i[1].set_footer(text=f"Pages Of {self._current_page}/{self._len}")
        if self._current_page == self._len:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        if self._current_page == 1:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        await interaction.message.edit(content=self._queue[0][0], view=self)

    @discord.ui.button(emoji="👈")
    async def previous(self, interaction: discord.Interaction, _):
        """
        Move to the previous page.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        self._queue.rotate(-1)
        msg, embed = self._queue[0]
        self._current_page -= 1
        await self.update_buttons(interaction)
        await interaction.message.edit(content=msg, embed=embed)

    @discord.ui.button(emoji="👉")
    async def next(self, interaction: discord.Interaction, _):
        """
        Move to the next page.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        self._queue.rotate(1)
        msg, embed = self._queue[0]
        self._current_page += 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(content=msg, embed=embed)

    @property
    def initial(self) -> tuple:
        """
        Get the initial tuple.

        Returns:
            tuple: The initial tuple containing a string and an embed.
        """
        return self._initial
'''

class PaginatorViewNasheed(PaginatorView):
    def __init__(self,embeds:List[discord.Embed]):
        super().__init__(embeds)


    @discord.ui.button(emoji="⏬")
    async def download(self,interaction:discord.Interaction,_):
        await interaction.response.defer()
        current_embed  = self._embeds[(self._current_page - 1)]
        ic(self._embeds)
        ic(self._current_page)
        ic(self._queue)
        current_embed = current_embed.to_dict()["fields"]
        ic(current_embed)
        down_link = current_embed[5]["value"]
        ic(down_link)
        down_link=  down_link.split("|| *")[0].replace("||","")
        ic(down_link)
        async with aiohttp.ClientSession() as session:
            async with session.get(down_link) as resp:
                if resp.status == 200:
                    total_size = int(resp.headers.get('Content-Length', 0))
                    mu = io.BytesIO()
                    downloaded = 0
                    channel = interaction.channel
                    msg = await channel.send("PROGRESS BAR...")

                    async for chunk in resp.content.iter_chunks() :  # Adjust the chunk size as needed
                        mu.write(chunk[0])
                        downloaded += len(chunk[0])
                        percentage = (downloaded / total_size) * 100
                        ic(percentage)
                        await msg.edit(content="",embed=create_embed("Progress",create_ratio_string(percentage),discord.Color.yellow()))
                    mu.seek(0)
                    await msg.edit(content="",embed=create_embed("Uploading","Uploading...",discord.Color.green()))
                    file  = discord.File(fp=mu,filename=current_embed[6]["value"].replace("||",""))
                    await channel.send(f'||{current_embed[6]["value"].replace("||","")}||',file=file)
                    await msg.delete()



    @property
    def initial(self)-> discord.Embed:
        return self._initial

