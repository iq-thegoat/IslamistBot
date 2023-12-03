import discord
from discord import app_commands, File
from discord.ext import commands
from discord.ext import tasks
from blur_cmnds import blur_vid, blur_img
from funks import create_ratio_string, create_embed


class Blur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blur_video")
    @app_commands.describe(
        blur_strength="the strength of the blur",
        video="the video you want to blur",
        message="caption",
        url="the url of a video on one of these platforms[Tiktok,Youtube]",
    )
    @app_commands.choices(
        blur_strength=[
            app_commands.Choice(name="low", value=10),
            app_commands.Choice(name="moderate", value=15),
            app_commands.Choice(name="medium", value=20),
            app_commands.Choice(name="high", value=25),
            app_commands.Choice(name="SUPER", value=30),
            app_commands.Choice(name="EXTREME", value=35),
            app_commands.Choice(name="MAXIMUM", value=50),
            app_commands.Choice(name="OVERKILL", value=100),
        ]
    )
    async def blur_video(
        self,
        interaction: discord.Interaction,
        blur_strength: app_commands.Choice[int],
        video: discord.Attachment = None,
        message: str = " ",
        url: str = None,
    ):
        await interaction.response.send_message(
            embed=create_embed("Working On it...", "", discord.Color.green()),
            ephemeral=True,
        )
        if video:
            resp = await blur_vid(
                video, strength=int(blur_strength.value), interaction=interaction
            )
        else:
            resp = await blur_vid(
                url, strength=int(blur_strength.value), interaction=interaction
            )

        if isinstance(resp, tuple):
            member = interaction.user
            webhook = await interaction.channel.create_webhook(name=member.name)
            await webhook.send(
                str(message),
                file=File(resp[0], resp[1]),
                username=member.name,
                avatar_url=member.avatar.url,
            )
            await interaction.delete_original_response()
            await webhook.delete()
        else:
            await interaction.edit_original_response(
                embed=create_embed("Error", resp, color=discord.Color.red())
            )

    @app_commands.command(name="blur_image")
    @app_commands.describe(
        message="caption",
        blur_strength="the strength of the blur",
        image="the image you want to blur",
    )
    @app_commands.choices(
        blur_strength=[
            app_commands.Choice(name="low", value=6),
            app_commands.Choice(name="moderate", value=10),
            app_commands.Choice(name="medium", value=14),
            app_commands.Choice(name="high", value=22),
        ]
    )
    async def _blur_image(
        self,
        interaction: discord.Interaction,
        blur_strength: app_commands.Choice[int],
        image: discord.Attachment,
        message: str = " ",
    ):
        await interaction.response.send_message(
            embed=create_embed("Working On it...", "", discord.Color.green()),
            ephemeral=True,
        )
        resp = await blur_img(image, radius=int(blur_strength.value))
        if isinstance(resp, tuple):
            member = interaction.user
            webhook = await interaction.channel.create_webhook(name=member.name)
            await webhook.send(
                str(message),
                file=File(resp[0], resp[1]),
                username=member.name,
                avatar_url=member.avatar.url,
            )
            await interaction.delete_original_response()
            webhooks = await interaction.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
        else:
            await interaction.edit_original_response(
                embed=create_embed("Error", resp, color=discord.Color.red())
            )


async def setup(bot):
    await bot.add_cog(Blur(bot=bot))
