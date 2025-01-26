import json
import os
import random
import platform
from status import *
from config import *

def close_running_processes(process_name: str = "firefox") -> None:
    """
    Closes any running instances of the specified process.

    Args:
        process_name (str): Name of the process to close. Default is "firefox".

    Returns:
        None
    """
    try:
        info(f" => Closing running {process_name} instances...")

        if platform.system() == "Windows":
            os.system(f"taskkill /f /im {process_name}.exe")
        else:
            os.system(f"pkill {process_name}")

        success(f" => Closed running {process_name} instances.")
    except Exception as e:
        error(f"Error occurred while closing {process_name} instances: {str(e)}")

def build_url(youtube_video_id: str) -> str:
    """
    Builds the URL to the YouTube video.

    Args:
        youtube_video_id (str): The YouTube video ID.

    Returns:
        str: The URL to the YouTube video.
    """
    return f"https://www.youtube.com/watch?v={youtube_video_id}"

def rem_temp_files() -> None:
    """
    Removes temporary files in the `.mp` directory.

    Returns:
        None
    """
    mp_dir = os.path.join(ROOT_DIR, ".mp")
    if not os.path.exists(mp_dir):
        warning(f"The directory {mp_dir} does not exist.")
        return

    files = os.listdir(mp_dir)
    for file in files:
        file_path = os.path.join(mp_dir, file)
        if os.path.isfile(file_path) and not file.endswith(".json"):
            os.remove(file_path)

    success(f" => Removed temporary files from {mp_dir}.")

def ensure_songs_directory() -> None:
    """
    Ensures that the `Songs` directory exists and contains sample songs.

    Returns:
        None
    """
    songs_dir = os.path.join(ROOT_DIR, "Songs")
    if not os.path.exists(songs_dir):
        os.mkdir(songs_dir)
        success(f" => Created directory: {songs_dir}")

    # Check if directory is empty
    if not os.listdir(songs_dir):
        warning(f"The {songs_dir} directory is empty. Add songs manually to use this feature.")
    else:
        info(f" => Songs directory is ready: {songs_dir}")

def choose_random_song() -> str:
    """
    Chooses a random song from the `Songs` directory.

    Returns:
        str: The path to the chosen song.
    """
    try:
        songs_dir = os.path.join(ROOT_DIR, "Songs")
        songs = os.listdir(songs_dir)
        if not songs:
            raise FileNotFoundError(f"No songs found in the {songs_dir} directory.")
        
        song = random.choice(songs)
        success(f" => Chose song: {song}")
        return os.path.join(songs_dir, song)
    except Exception as e:
        error(f"Error occurred while choosing a random song: {str(e)}")
        return ""

def load_api_keys(secret_file: str) -> dict:
    """
    Loads API keys from the secret file.

    Args:
        secret_file (str): Path to the secret file.

    Returns:
        dict: Dictionary of API keys.
    """
    try:
        with open(secret_file, "r") as file:
            data = json.load(file)
            if "web" in data and "openai_api_key" in data["web"]:
                success("API keys loaded successfully.")
            else:
                warning("API keys file is missing 'openai_api_key' under 'web'.")
            return data["web"]
    except json.JSONDecodeError as e:
        error(f"JSON decoding error: {e}")
        return {}
    except FileNotFoundError as e:
        error(f"Secret file not found: {e}")
        return {}
    except Exception as e:
        error(f"Failed to load API keys from {secret_file}: {str(e)}")
        return {}
