import os
import sys
import json
import srt_equalizer

from termcolor import colored

ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


def assert_folder_structure() -> None:
    """
    Ensures necessary folder structure is present.
    """
    mp_dir = os.path.join(ROOT_DIR, ".mp")
    if not os.path.exists(mp_dir):
        print(colored(f"=> Creating .mp folder at {mp_dir}", "green"))
        os.makedirs(mp_dir)


def get_first_time_running() -> bool:
    """
    Checks if the program is running for the first time.

    Returns:
        bool: True if first-time run, False otherwise.
    """
    return not os.path.exists(os.path.join(ROOT_DIR, ".mp"))


def _get_config_value(key: str):
    """
    Generic function to fetch a value from `config.json`.

    Args:
        key (str): The key to fetch.

    Returns:
        Any: The value associated with the key.
    """
    config_path = os.path.join(ROOT_DIR, "config.json")
    with open(config_path, "r") as file:
        config = json.load(file)
        return config.get(key)


# Configuration getters
def get_email_credentials() -> dict:
    return _get_config_value("email")


def get_verbose() -> bool:
    return _get_config_value("verbose")


def get_headless() -> bool:
    return _get_config_value("headless")


def get_model() -> str:
    return _get_config_value("llm")


def get_image_prompt_llm() -> str:
    return _get_config_value("image_prompt_llm")


def get_image_model() -> str:
    return _get_config_value("image_model")


def get_threads() -> int:
    return _get_config_value("threads")


def get_zip_url() -> str:
    return _get_config_value("zip_url")


def get_is_for_kids() -> bool:
    return _get_config_value("is_for_kids")


def get_scraper_timeout() -> int:
    return _get_config_value("scraper_timeout") or 300


def get_outreach_message_subject() -> str:
    return _get_config_value("outreach_message_subject")


def get_outreach_message_body_file() -> str:
    return _get_config_value("outreach_message_body_file")


def get_assemblyai_api_key() -> str:
    return _get_config_value("assembly_ai_api_key")


def get_google_maps_scraper_zip_url() -> str:
    return _get_config_value("google_maps_scraper")


def get_google_maps_scraper_niche() -> str:
    return _get_config_value("google_maps_scraper_niche")


def get_font() -> str:
    return _get_config_value("font")


def get_fonts_dir() -> str:
    """
    Returns the fonts directory.
    """
    return os.path.join(ROOT_DIR, "fonts")


def get_imagemagick_path() -> str:
    return _get_config_value("imagemagick_path")


# Subtitle processing
def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
    """
    Equalizes subtitles in an SRT file.

    Args:
        srt_path (str): Path to the SRT file.
        max_chars (int): Max characters per subtitle.
    """
    srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)
