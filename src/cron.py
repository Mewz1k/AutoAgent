import sys
from status import *
from cache import get_accounts
from config import get_verbose
from classes.Tts import TTS
from classes.YouTube import YouTube

def main():
    """
    Main function to handle CRON tasks for YouTube automation.

    Purpose: Automates video generation and upload for YouTube accounts.

    Args:
        sys.argv[1]: Purpose ('youtube')
        sys.argv[2]: Account UUID
    """
    if len(sys.argv) < 3:
        error("Invalid arguments. Usage: cron.py <purpose> <account_id>")
        sys.exit(1)

    purpose = sys.argv[1].strip().lower()
    account_id = sys.argv[2].strip()

    verbose = get_verbose()

    if purpose == "youtube":
        tts = TTS()

        # Fetch YouTube accounts from cache
        accounts = get_accounts("youtube")

        if not account_id:
            error("Account UUID cannot be empty.")
            sys.exit(1)

        account_found = False
        for acc in accounts:
            if acc["id"] == account_id:
                account_found = True
                if verbose:
                    info("Initializing YouTube automation...")

                youtube = YouTube(
                    acc["id"],
                    acc["nickname"],
                    acc["niche"],
                    acc["language"]
                )

                try:
                    video_path = youtube.generate_video(tts)
                    youtube.upload_video(video_path)
                    if verbose:
                        success("YouTube Short successfully uploaded.")
                except Exception as e:
                    error(f"Error during YouTube automation: {str(e)}")
                break

        if not account_found:
            error(f"No YouTube account found with ID: {account_id}")
            sys.exit(1)

    else:
        error("Invalid purpose specified. Supported: 'youtube'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
