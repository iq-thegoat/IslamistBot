import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
from icecream import ic
from funks import config
import os


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is up and ready!")
    await bot.load_extension("Noor")
    await bot.load_extension("Blur")
    await bot.load_extension("Dorrar")
    await bot.load_extension("Islamway_Anasheed")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        logger.error(str(e))

bot.run(
    token="MTAzNDQ3MzU4NDk1OTE2NDQ1Ng.GL4XJw.4Fk2F6fmGB8OpNqk5_trY9OnqSnvSM5lYytYQE"
)
