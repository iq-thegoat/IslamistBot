import os
import subprocess
import io
from loguru import logger
import re
from PIL import Image, ImageFilter
from apis import YoutubeDownloader, TiktokDownloader, generate_random_file_id
import discord
from funks import download_attachment, create_embed, create_ratio_string
from urllib.parse import urlparse


def calculate_percentage(frame, total_frames):
    return (frame / total_frames) * 100


from moviepy.editor import VideoFileClip


def get_total_frames(input_file):
    try:
        # Open the video file
        clip = VideoFileClip(input_file)

        # Get the total number of frames
        total_frames = int(clip.fps * clip.duration)

        # Close the video clip
        clip.close()
        print(str("TOTALFRAMES " + str(total_frames)))
        return total_frames

    except Exception as e:
        raise ValueError(f"Unable to get total frames from the input video. Error: {e}")


def apply_blur_effect(input_file, output_file, strength):
    """
    Apply a blur effect to a video file using FFmpeg.

    Parameters:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output video file.
    - strength (int): Strength of the blur effect.
    - applies (int): Number of times the blur effect is applied.

    Returns:
    - str: Data of the resulting video file.
    """

    try:
        total_frames = get_total_frames(input_file)
        # Construct the FFmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            input_file,
            "-vf",
            f"gblur=sigma={strength}",
            "-c:a",
            "copy",
            output_file,
            "-y",
        ]

        # Execute the FFmpeg command using subprocess
        process = subprocess.Popen(
            ffmpeg_command, stderr=subprocess.PIPE, universal_newlines=True
        )

        # Regular expression to extract progress information
        progress_regex = re.compile(
            r"frame=\s*(\d+)\s*fps=\s*([\d.]+)\s*q=\s*([\d.]+)\s*L?size=\s*([\d.]+[kKmMgG]?)\s*"
        )

        while True:
            line = process.stderr.readline()
            if not line:
                break
            match = progress_regex.search(line)
            if match:
                frame = int(match.group(1))
                percentage = calculate_percentage(frame, total_frames=total_frames)
                yield percentage

        # Wait for the process to complete
        process.wait()

        # Read the resulting video file data
        with open(output_file, "rb") as f:
            video_data = f.read()
        os.remove(input_file)
        os.remove(output_file)
        yield io.BytesIO(video_data)

    except subprocess.CalledProcessError as e:
        print(f"Error: FFmpeg command failed with return code {e.returncode}.")
        return None


def apply_blur_effect_img(input_path, radius=2):
    # Open the image file
    img = Image.open(input_path)

    # Convert the image to RGB mode if it's in RGBA mode
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Apply Gaussian blur
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius))

    output_bytesio = io.BytesIO()
    blurred_img.save(output_bytesio, format="JPEG")

    # Set the file pointer to the beginning of the BytesIO object
    output_bytesio.seek(0)

    return output_bytesio


async def blur_vid(
    attachment: discord.Attachment or str,
    strength: int,
    interaction: discord.Interaction,
):
    if isinstance(attachment, discord.Attachment):
        if attachment.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
            if await download_attachment(attachment):
                output = (
                    os.path.split(attachment.filename)[0]
                    + "edited"
                    + os.path.split(attachment.filename)[1]
                )
                for percentage in apply_blur_effect(
                    input_file=attachment.filename,
                    output_file=output,
                    strength=strength,
                ):
                    print("PERCENTAGE" + str(percentage))
                    if isinstance(percentage, int) or isinstance(percentage, float):
                        await interaction.edit_original_response(
                            embed=create_embed(
                                "Percentage",
                                create_ratio_string(percentage),
                                discord.Color.gold(),
                            )
                        )
                    elif isinstance(percentage, io.BytesIO):
                        vid = percentage
                        await interaction.edit_original_response(
                            embed=create_embed(
                                "Uploading",
                                "finished blurring, uploading...",
                                discord.Color.green(),
                            )
                        )
                        break
                    else:
                        vid = percentage
                return (vid, attachment.filename)

            else:
                return "Couldn't download the video, sorry good luck next time"

        else:
            return "attachment must be a video in one of these filetypes ('.mp4', '.mov', '.avi', '.mkv')"

    elif isinstance(attachment, str):
        name = generate_random_file_id() + ".mp4"
        try:
            parsed_url = urlparse(attachment)
            domain = parsed_url.netloc
        except:
            return "please use a valid url with the following format [scheme]://[domain]/[path]"
        if domain.lower() == "www.tiktok.com":
            data = TiktokDownloader.download(url=attachment, output=name)
        elif domain.lower() == "youtube.com" or domain.lower() == "www.youtube.com":
            data = YoutubeDownloader.download(url=attachment, output=name)

        output = os.path.split(name)[0] + "edited" + os.path.split(name)[1]
        if data:
            print(data)
            for percentage in apply_blur_effect(
                input_file=name, output_file=output, strength=strength
            ):
                if isinstance(percentage, int) or isinstance(percentage, float):
                    await interaction.edit_original_response(
                        embed=create_embed(
                            "Percentage",
                            create_ratio_string(percentage),
                            discord.Color.gold(),
                        )
                    )
                elif isinstance(percentage, io.BytesIO):
                    vid = percentage
                    await interaction.edit_original_response(
                        embed=create_embed(
                            "Uploading",
                            "finished blurring, now uploading...",
                            discord.Color.green(),
                        )
                    )
                else:
                    vid = percentage
            return (vid, name)


async def blur_img(attachment: discord.Attachment, radius: int):
    if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        if await download_attachment(attachment):
            IMGIO = apply_blur_effect_img(attachment.filename, radius)
            if IMGIO:
                return (IMGIO, attachment.filename)
            else:
                return False
