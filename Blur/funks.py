import aiohttp
import discord
from typing import Union


async def download_attachment(attachment):
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


def create_embed(title: str, content: str, color: discord.Color):
    embed = discord.Embed(title=title, color=color)
    embed.add_field(name=content, value="")
    print(type(embed))
    return embed


def create_ratio_string(
    percentage: Union[int, float],
    upchar: str = "🟩",
    downchar: str = "🟥",
):
    percentage = int(percentage)
    win_string = upchar * (percentage // 10)
    win_string = win_string + (downchar * (10 - len(win_string)))
    print(win_string)
    return f"progress:{win_string} ({round((percentage),2)}%)"
