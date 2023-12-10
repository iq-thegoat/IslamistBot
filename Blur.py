import discord
from discord import app_commands, File
from discord.ext import commands
from discord.ext import tasks
from blur_cmnds import blur_vid, blur_img
from funks import create_embed
from icecream import ic


class Blur(commands.Cog):
    """
    A Discord cog for blurring videos and images.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the Blur cog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="blur_video")
    @app_commands.describe(
        blur_strength="the strength of the blur",
        video="the video you want to blur",
        part="wether to blur the [top] half or the [lower] half or [all] of the video",
        message="caption",
        url="the url of a video on one of these platforms[Tiktok,Youtube]",
    )
    @app_commands.choices(
        part=[
            app_commands.Choice(name="top", value=1),
            app_commands.Choice(name="all", value=2),
            # app_commands.Choice(name="bottom",value=3), #need to be fixed
        ]
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
        part: app_commands.Choice[int],
        video: discord.Attachment = None,
        message: str = " ",
        url: str = None,
    ):
        """
        Blur a video and send the result with a caption.

        Args:
            interaction (discord.Interaction): The interaction object.
            blur_strength (app_commands.Choice[int]): The strength of the blur effect.
            video (discord.Attachment): The video attachment to blur.
            message (str): The caption to include with the blurred video.
            url (str): The URL of the video on TikTok or YouTube.

        Returns:
            None
        """
        part = part.name
        await interaction.response.send_message(
            embed=await create_embed("Working On it...", "", discord.Color.green()),
            ephemeral=True,
        )
        if video:
            resp = await blur_vid(
                video,
                strength=int(blur_strength.value),
                interaction=interaction,
                part=part,
            )
        else:
            resp = await blur_vid(
                url,
                strength=int(blur_strength.value),
                interaction=interaction,
                part=part,
            )
        ic(resp)
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
                embed=await create_embed("Error", resp, color=discord.Color.red())
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
        """
        Blur an image and send the result with a caption.

        Args:
            interaction (discord.Interaction): The interaction object.
            blur_strength (app_commands.Choice[int]): The strength of the blur effect.
            image (discord.Attachment): The image attachment to blur.
            message (str): The caption to include with the blurred image.

        Returns:
            None
        """
        await interaction.response.send_message(
            embed=await create_embed("Working On it...", "", discord.Color.green()),
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
                embed=await create_embed("Error", resp, color=discord.Color.red())
            )


async def setup(bot):
    """
    Setup function for adding the Blur cog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.

    Returns:
        None
    """
    await bot.add_cog(Blur(bot=bot))
