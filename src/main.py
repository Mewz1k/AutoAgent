import os
import re
import sys
import schedule
import subprocess
import openai
from art import *
from cache import *
from utils import *
from config import *
from status import *
from uuid import uuid4
from constants import *
from classes.Tts import TTS
from termcolor import colored
from classes.Twitter import Twitter
from classes.YouTube import YouTube
from prettytable import PrettyTable
from classes.Outreach import Outreach
from classes.AFM import AffiliateMarketing
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json


def main():
    """
    Main function to display the menu and handle user input.
    """
    # Setup Google Auth using the secret_client.json file
    credentials = service_account.Credentials.from_service_account_info(
        API_KEYS["google_credentials"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_request = Request()
    credentials.refresh(auth_request)

    valid_input = False
    while not valid_input:
        try:
            # Show user options
            info("\n============ OPTIONS ============", False)
            for idx, option in enumerate(OPTIONS):
                print(colored(f" {idx + 1}. {option}", "cyan"))
            info("=================================\n", False)

            user_input = input("Select an option: ").strip()
            if user_input == '':
                raise ValueError("Empty input is not allowed.")
            user_input = int(user_input)
            valid_input = True
        except ValueError as e:
            print("\n" * 100)
            print(f"Invalid input: {e}")

    # Process user input
    if user_input == 1:
        handle_youtube_flow()
    elif user_input == 2:
        handle_twitter_flow()
    elif user_input == 3:
        handle_affiliate_marketing_flow()
    elif user_input == 4:
        handle_outreach_flow()
    elif user_input == 5:
        if get_verbose():
            print(colored(" => Quitting...", "blue"))
        sys.exit(0)
    else:
        error("Invalid option selected. Please try again.", "red")
        main()


def handle_youtube_flow():
    """
    Handle YouTube Shorts automation workflow.
    """
    info("Starting YT Shorts Automater...")
    cached_accounts = get_accounts("youtube")

    if len(cached_accounts) == 0:
        warning("No accounts found in cache. Create one now?")
        user_input = question("Yes/No: ")
        if user_input.lower() == "yes":
            add_youtube_account()
    else:
        selected_account = select_account(cached_accounts, "youtube")
        if not selected_account:
            return

        youtube = YouTube(
            account_uuid=selected_account["id"],
            account_nickname=selected_account["nickname"],
            niche=selected_account["niche"],
            language=selected_account["language"]
        )
        while True:
            rem_temp_files()
            info("\n============ YOUTUBE OPTIONS ============", False)
            for idx, youtube_option in enumerate(YOUTUBE_OPTIONS):
                print(colored(f" {idx + 1}. {youtube_option}", "cyan"))
            info("=========================================\n", False)

            user_input = int(question("Select an option: "))
            tts = TTS()

            if user_input == 1:
                video_path = youtube.generate_video(tts)
                upload_to_yt = question("Do you want to upload this video to YouTube? (Yes/No): ")
                if upload_to_yt.lower() == "yes":
                    youtube.upload_video(video_path)
            elif user_input == 2:
                videos = youtube.get_videos()
                if videos:
                    display_videos_table(videos)
                else:
                    warning("No videos found.")
            elif user_input == 3:
                schedule_youtube_cron(youtube)
            elif user_input == 4:
                break


def add_youtube_account():
    """
    Add a new YouTube account to the cache.
    """
    generated_uuid = str(uuid4())
    success(f" => Generated ID: {generated_uuid}")
    nickname = question(" => Enter a nickname for this account: ")
    niche = question(" => Enter the account niche: ")
    language = question(" => Enter the account language: ")

    add_account("youtube", {
        "id": generated_uuid,
        "nickname": nickname,
        "niche": niche,
        "language": language,
        "videos": []
    })


def select_account(cached_accounts, platform):
    """
    Select an account from the cached accounts.

    Args:
        cached_accounts (list): List of cached accounts.
        platform (str): Platform name (YouTube/Twitter).

    Returns:
        dict: Selected account information.
    """
    table = PrettyTable()
    table.field_names = ["ID", "UUID", "Nickname", "Niche/Topic"]
    for account in cached_accounts:
        table.add_row([
            cached_accounts.index(account) + 1,
            colored(account["id"], "cyan"),
            colored(account["nickname"], "blue"),
            colored(account["niche"] if platform == "youtube" else account["topic"], "green")
        ])
    print(table)

    user_input = question(f"Select an account to start ({platform}): ")
    for account in cached_accounts:
        if str(cached_accounts.index(account) + 1) == user_input:
            return account
    error("Invalid account selected. Please try again.", "red")
    return None


def display_videos_table(videos):
    """
    Display the table of videos.

    Args:
        videos (list): List of videos to display.
    """
    videos_table = PrettyTable()
    videos_table.field_names = ["ID", "Date", "Title"]
    for video in videos:
        videos_table.add_row([
            videos.index(video) + 1,
            colored(video["date"], "blue"),
            colored(video["title"][:60] + "...", "green")
        ])
    print(videos_table)


def schedule_youtube_cron(youtube):
    """
    Schedule a CRON job for YouTube uploads.

    Args:
        youtube (YouTube): Instance of the YouTube class.
    """
    info("How often do you want to upload?")
    info("\n============ SCHEDULE OPTIONS ============", False)
    for idx, cron_option in enumerate(YOUTUBE_CRON_OPTIONS):
        print(colored(f" {idx + 1}. {cron_option}", "cyan"))
    info("=========================================\n", False)

    user_input = int(question("Select an Option: "))
    if user_input == 1:
        schedule.every(1).day.do(youtube.upload_video)
        success("Set up daily upload CRON Job.")
    elif user_input == 2:
        schedule.every().day.at("10:00").do(youtube.upload_video)
        schedule.every().day.at("16:00").do(youtube.upload_video)
        success("Set up twice-daily upload CRON Job.")


if __name__ == "__main__":
    # Print ASCII Banner
    print_banner()

    first_time = get_first_time_running()
    if first_time:
        print(colored("Hey! Welcome to AutoAgent. Let's set things up for you!", "yellow"))

    # Setup file tree and remove temporary files
    assert_folder_structure()
    rem_temp_files()

    # Fetch MP3 Files (stored in 'songs' folder)
    fetch_songs()

    while True:
        main()
