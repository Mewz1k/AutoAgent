"""
This file contains all the constants used in the program.
"""

OPTIONS = [
    "YouTube Shorts Automation",
    "Twitter Bot",
    "Affiliate Marketing",
    "Outreach",
    "Quit"
]

YOUTUBE_OPTIONS = [
    "Upload Short",
    "Show all Shorts",
    "Setup CRON Job",
    "Quit"
]

YOUTUBE_CRON_OPTIONS = [
    "Once a day",
    "Twice a day",
    "Thrice a day",
    "Quit"
]

# API Models
SUPPORTED_LLM_MODELS = {
    "gpt4": "gpt-4",
    "gpt35_turbo": "gpt-3.5-turbo",
    "llama2_7b": "llama2-7b",
    "llama2_13b": "llama2-13b",
    "llama2_70b": "llama2-70b",
    "mixtral_8x7b": "mixtral-8x7b"
}

# YouTube Section
YOUTUBE_MADE_FOR_KIDS = {
    "yes": "VIDEO_MADE_FOR_KIDS_MFK",
    "no": "VIDEO_MADE_FOR_KIDS_NOT_MFK"
}
YOUTUBE_BUTTON_IDS = {
    "textbox": "textbox",
    "next": "next-button",
    "done": "done-button",
}
YOUTUBE_RADIO_BUTTON_XPATH = "//*[@id=\"radioLabel\"]"

# Helper Functions
def parse_model(model_name: str) -> str:
    """
    Parses the model name and returns the corresponding OpenAI model.

    Args:
        model_name (str): The user-provided model name.

    Returns:
        str: The matching model identifier.
    """
    return SUPPORTED_LLM_MODELS.get(model_name.lower(), "gpt-3.5-turbo")
