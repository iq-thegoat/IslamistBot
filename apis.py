import requests
from bs4 import BeautifulSoup
from pathlib import Path
import io
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
import uuid


def generate_random_file_id():
    """
    Generates a random file ID using a UUID.

    Returns:
        str: Random file ID.
    """
    file_id = str(uuid.uuid4())
    return file_id


class TiktokDownloader:
    @staticmethod
    def download(url: str, output: str):
        """
        Downloads a TikTok video from the provided URL.

        Args:
            url (str): TikTok video URL.
            output (str): Output file path for the downloaded video.

        Returns:
            Union[str, bool]: Output file path on success, False on failure.
        """
        video_id = url.split("video/")[1].split("?")[0]

        if video_id:
            print(video_id)
            # Construct a new URL
            tiktok_url = f"https://tikcdn.io/ssstik/{video_id}"

            # Make the request and handle errors
            try:
                r = requests.get(url=tiktok_url, stream=True)
                r.raise_for_status()  # Raise an exception for bad responses
                print(r.status_code)
                # Download the content into a BytesIO object
                with open(output, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                return output
            except requests.exceptions.RequestException as e:
                return False
        else:
            return False


class YoutubeDownloader:
    @staticmethod
    def download(url: str, output: str):
        """
        Downloads a YouTube video from the provided URL.

        Args:
            url (str): YouTube video URL.
            output (str): Output file path for the downloaded video.

        Returns:
            Union[str, bool]: True on success, error message on failure.
        """
        try:
            # Create a YouTube object
            video_stream = YouTube(url).streams.get_highest_resolution()
            video_stream.download(output_path=".", filename=output)
            return True
        except Exception as e:
            return f"Error: {e}"

# Example usage (uncomment if needed)
# if __name__ == "__main__":
#     TiktokDownloader.download(url="https://www.tiktok.com/@hazim_shwman1/video/7292853003709664518?is_from_webapp=1&sender_device=pc", output=generate_random_file_id() + ".mp4")
#     d = YoutubeDownloader.download(url="https://www.youtube.com/shorts/72MYQo4IUNg", output_path=generate_random_file_id() + ".mp4")
#     print(d)
