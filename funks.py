import discord
import json
import aiohttp
from typing import Union
import functools
from functools import lru_cache
import pickle


async def create_embed(title: str, content: str, color: discord.Color):
    """
    Create and return a Discord embed with the specified title, content, and color.

    Args:
        title (str): The title of the embed.
        content (str): The content of the embed.
        color (discord.Color): The color of the embed.

    Returns:
        discord.Embed: The created embed.
    """
    embed = discord.Embed(title=title, color=color)
    embed.add_field(name=content, value="")
    return embed


async def config() -> dict:
    """
    Read and return the contents of the "Config.json" file as a dictionary.

    Returns:
        dict: The contents of the "Config.json" file.
    """
    with open("Config.json", "r") as f:
        return json.load(f)


async def download_attachment(attachment):
    """
    Download the provided Discord attachment.

    Args:
        attachment: The Discord attachment to download.

    Returns:
        bool: True if the download is successful, False otherwise.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as resp:
            if resp.status == 200:
                data = await resp.read()
                # You can save the video to a file or process it as needed
                with open(f"{attachment.filename}", "wb") as f:
                    f.write(data)
                return True
            else:
                return False


async def create_ratio_string(
    percentage: Union[int, float],
    upchar: str = "🟩",
    downchar: str = "🟥",
):
    """
    Create and return a progress string based on the given percentage.

    Args:
        percentage (Union[int, float]): The percentage value.
        upchar (str): The character to represent the filled part of the progress bar.
        downchar (str): The character to represent the empty part of the progress bar.

    Returns:
        str: The progress string.
    """
    percentage = int(percentage)
    win_string = upchar * (percentage // 10)
    win_string = win_string + (downchar * (10 - len(win_string)))
    return f"progress:{win_string} ({round((percentage), 2)}%)"
