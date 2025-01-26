import os
from config import ROOT_DIR
from google.cloud import texttospeech

class TTS:
    """
    Class for Text-to-Speech using Google Cloud Text-to-Speech.
    """
    def __init__(self) -> None:
        """
        Initializes the TTS class.
        """
        # Set up Google Text-to-Speech client
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, text: str, output_file: str = os.path.join(ROOT_DIR, ".mp", "audio.wav")) -> str:
        """
        Synthesizes the given text into speech using Google Cloud Text-to-Speech.

        Args:
            text (str): The text to synthesize.
            output_file (str, optional): The output file to save the synthesized speech. Defaults to "audio.wav".

        Returns:
            str: The path to the output file.
        """
        # Configure synthesis input
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Set voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",  # Change to desired language
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        # Set audio configuration
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform text-to-speech request
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the synthesized speech to the output file
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        return output_file
