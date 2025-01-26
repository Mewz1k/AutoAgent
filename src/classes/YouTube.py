import os
import re
import json
import requests
import openai
import assemblyai as aai

from utils import *
from cache import *
from classes.Tts import TTS
from config import *
from status import *
from uuid import uuid4
from constants import *
from typing import List
from moviepy.editor import *
from termcolor import colored
from moviepy.video.fx.all import crop
from moviepy.config import change_settings
from moviepy.video.tools.subtitles import SubtitlesClip
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

# Set ImageMagick Path
change_settings({"IMAGEMAGICK_BINARY": get_imagemagick_path()})

# Load API Keys
SECRET_FILE = "secret_client.json"
API_KEYS = load_api_keys(SECRET_FILE)

# Configure OpenAI API
openai.api_key = API_KEYS["openai_api_key"]

class YouTube:
    """
    Class for YouTube Automation.
    """
    def __init__(self, account_uuid: str, account_nickname: str, niche: str, language: str) -> None:
        """
        Constructor for YouTube Class.

        Args:
            account_uuid (str): The unique identifier for the YouTube account.
            account_nickname (str): The nickname for the YouTube account.
            niche (str): The niche of the provided YouTube Channel.
            language (str): The language of the Automation.
        """
        self._account_uuid = account_uuid
        self._account_nickname = account_nickname
        self._niche = niche
        self._language = language
        self.images = []

        # Google API Client Setup
        self.credentials = Credentials.from_service_account_info(
            API_KEYS["google_credentials"],
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        self.youtube_service = build("youtube", "v3", credentials=self.credentials)

    @property
    def niche(self) -> str:
        return self._niche

    @property
    def language(self) -> str:
        return self._language

    def generate_response(self, prompt: str) -> str:
        """
        Generates an LLM Response based on a prompt using OpenAI API.

        Args:
            prompt (str): The prompt to use in the text generation.

        Returns:
            response (str): The generated AI Response.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            error(f"OpenAI API error: {e}")
            return ""

    def generate_topic(self) -> str:
        """
        Generates a topic based on the YouTube Channel niche.

        Returns:
            topic (str): The generated topic.
        """
        prompt = f"Generate a specific video idea about the following topic: {self.niche}."
        completion = self.generate_response(prompt)
        if not completion:
            error("Failed to generate Topic.")
        self.subject = completion
        return completion

    def generate_script(self) -> str:
        """
        Generate a script for a video based on the subject of the video.

        Returns:
            script (str): The script of the video.
        """
        prompt = f"""
        Generate a short 4-sentence script for a video. The script must relate to this subject: {self.subject}. Use the language: {self.language}.
        Avoid unnecessary introductions and focus on the subject.
        """
        completion = self.generate_response(prompt)
        self.script = re.sub(r"\*", "", completion)
        return self.script

    def generate_metadata(self) -> dict:
        """
        Generates video metadata (Title, Description).

        Returns:
            metadata (dict): The generated metadata.
        """
        title_prompt = f"Create a concise, engaging YouTube title under 100 characters for: {self.subject}."
        description_prompt = f"Write a YouTube description for this script: {self.script}."

        title = self.generate_response(title_prompt)
        description = self.generate_response(description_prompt)

        self.metadata = {"title": title, "description": description}
        return self.metadata

    def generate_prompts(self) -> List[str]:
        """
        Generates AI Image Prompts based on the provided video script.

        Returns:
            image_prompts (List[str]): List of generated prompts.
        """
        prompt = f"Generate three detailed image prompts for AI image generation based on this script: {self.script}."
        response = self.generate_response(prompt)
        self.image_prompts = json.loads(response)
        return self.image_prompts

    def generate_image(self, prompt: str) -> str:
        """
        Generates an AI image based on the given prompt.

        Args:
            prompt (str): Reference for image generation.

        Returns:
            path (str): The path to the generated image.
        """
        image_path = os.path.join(ROOT_DIR, "images", f"{uuid4()}.png")
        response = requests.post("https://api.openai.com/v1/images", json={"prompt": prompt})
        with open(image_path, "wb") as f:
            f.write(response.content)
        self.images.append(image_path)
        return image_path

    def upload_video(self, video_path: str, metadata: dict) -> None:
        """
        Uploads the video to YouTube using Google API.

        Args:
            video_path (str): The path to the video file.
            metadata (dict): Video metadata including title and description.
        """
        try:
            body = {
                "snippet": {
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "tags": ["YouTube Shorts", self.niche],
                    "categoryId": "22"
                },
                "status": {"privacyStatus": "unlisted"}
            }
            with open(video_path, "rb") as f:
                request = self.youtube_service.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=f
                )
                response = request.execute()
                success(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")
        except HttpError as e:
            error(f"An error occurred: {e}")

    def generate_video(self, tts_instance: TTS) -> str:
        """
        Generates a complete YouTube video.

        Args:
            tts_instance (TTS): Instance of TTS Class.

        Returns:
            path (str): The path to the final MP4 file.
        """
        self.generate_topic()
        self.generate_script()
        self.generate_metadata()
        self.generate_prompts()
        for prompt in self.image_prompts:
            self.generate_image(prompt)
        audio_path = self.generate_script_to_speech(tts_instance)
        video_path = self.combine(audio_path)
        return video_path
