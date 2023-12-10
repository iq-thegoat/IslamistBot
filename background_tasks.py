import os
import discord
from discord.ext import commands, tasks
from icecream import ic
import shutil

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.clear_cache.start()

    async def cog_load(self) -> None:
        self.clear_cache.stop()

    @tasks.loop(seconds=21600)  # every 6 hours reset the cache
    async def clear_cache(self):
        print("deleting tmp...")
        try:
            shutil.rmtree("tmp", ignore_errors=False, onerror=None)
            print("tmp deleted")
        except Exception as e:
            ic("Error clearing cache:", e)

def setup(bot):
    bot.add_cog(BackgroundTasks(bot))
