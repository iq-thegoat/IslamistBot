import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
from icecream import ic
from funks import config
import os

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = os.environ.get("token")


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


bot.run(token=TOKEN)
