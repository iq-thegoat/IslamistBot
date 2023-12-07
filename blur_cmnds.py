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
from icecream import ic

def calculate_percentage(frame, total_frames):
    """
    Calculate the percentage of processed frames.

    Args:
        frame (int): Current frame number.
        total_frames (int): Total number of frames in the video.

    Returns:
        float: Percentage of processed frames.
    """
    return (frame / total_frames) * 100


from moviepy.editor import VideoFileClip

def get_video_height(video_file):
    try:
        # Run FFmpeg command to get video information
        command = ["ffmpeg", "-i", video_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Extract video resolution from the output
        height_str = re.search(r"Stream.*Video:.* ([0-9]+)x([0-9]+)", result.stderr)
        
        if height_str:
            width, height = map(int, height_str.groups())
            return height
        else:
            ic("Unable to determine video resolution.")
            return None
    except Exception as e:
        ic(f"An error occurred: {str(e)}")
        return e


def get_total_frames(input_file):
    """
    Get the total number of frames in a video file.

    Args:
        input_file (str): Path to the input video file.

    Returns:
        int: Total number of frames.
    """
    try:
        # Open the video file
        clip = VideoFileClip(input_file)

        # Get the total number of frames
        total_frames = int(clip.fps * clip.duration)

        # Close the video clip
        clip.close()
        ic(str("TOTALFRAMES " + str(total_frames)))
        return total_frames

    except Exception as e:
        raise ValueError(f"Unable to get total frames from the input video. Error: {e}")

def apply_blur_effect(input_file, output_file, strength,part:str):
    """
    Apply a blur effect to a video file using FFmpeg.

    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to the output video file.
        strength (int): Strength of the blur effect.

    Yields:
        float or io.BytesIO: Yields percentage completion during processing and the resulting video data.
    """
    try:
        ic(part)
        total_frames = get_total_frames(input_file)
        if part == "all":    
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
        elif part == "top":
            
            #top_half_height = int(get_video_height(input_file) / 2)  
            # Command to blur the top half
            ffmpeg_command = [
            "ffmpeg",
            "-i",
            input_file,
            "-filter_complex",
            f"[0:v]crop=iw:ih/2:0:0[top];[top]gblur=sigma={strength}[blurred_top];[0:v][blurred_top]overlay=0:0[v]",
            "-map",
            "[v]",
            "-map",
            "0:a",  # Map all audio streams from the input file
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_file,
            "-y",
            ]


        elif part == "bottom":
            ffmpeg_command = [
                "ffmpeg",
                "-i",
                input_file,
                "-filter_complex",
                f"[0:v]crop=iw:ih/2:0:ih/2[bottom];[bottom]gblur=sigma={strength}[blurred_bottom];[0:v][blurred_bottom]overlay=0:ih/2[v];[0:a]anull[a]",
                "-map",
                "[v]",
                "-map",
                "[a]",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                output_file,
                "-y",
                ]
        ic(output_file)
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
        byts  = io.BytesIO(video_data)
        ic(len(byts.getvalue()))
        yield byts

    except subprocess.CalledProcessError as e:
        ic(f"Error: FFmpeg command failed with return code {e.returncode}.")
        return None

def apply_blur_effect_img(input_path, radius=2):
    """
    Apply a blur effect to an image file.

    Args:
        input_path (str): Path to the input image file.
        radius (int): Radius of the Gaussian blur.

    Returns:
        io.BytesIO: BytesIO object containing the resulting blurred image data.
    """
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
    part:str
):
    """
    Blur a video attachment or from a URL and update progress on Discord.

    Args:
        attachment (discord.Attachment or str): Video attachment or URL.
        strength (int): Strength of the blur effect.
        interaction (discord.Interaction): Discord interaction object.

    Returns:
        Tuple[io.BytesIO, str] or str: Tuple containing the resulting video data and filename on success, error message on failure.
    """
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
                    part=part
                ):
                    ic("PERCENTAGE" + str(percentage))
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
            ic(data)
            for percentage in apply_blur_effect(
                input_file=name, output_file=output, strength=strength,part=part
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
                    discord.Color.green(),))
                    return (vid,name)
                else:
                    vid = percentage
                    return (vid, name)

async def blur_img(attachment: discord.Attachment, radius: int):
    """
    # Blur an image attachment and return the resulting image data.
    Args:
    attachment (discord.Attachment): Image attachment.
    radius (int): Radius of the Gaussian blur.

    Returns:
        Tuple[io.BytesIO, str] or bool: Tuple containing the resulting image data and filename on success, False on failure.
    """
    if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        if await download_attachment(attachment):
            IMGIO = apply_blur_effect_img(attachment.filename, radius)
            if IMGIO:
                return (IMGIO, attachment.filename)
            else:
                return False
    else:
        return "attachment must be an image in one of these filetypes ('.jpg', '.jpeg', '.png', '.gif')"
