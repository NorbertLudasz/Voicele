from django.core.management.base import BaseCommand
from api.models import CantonesePhrase
import os
import json
import requests

class Command(BaseCommand):

    def save_audio(self, filename, audio_data, directory='frontend/static/soundfiles'):
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as audio_file:
            audio_file.write(audio_data)

    def generate_audio_for_phrases(self):
        headers = {}
        url = "https://api.edenai.run/v2/audio/text_to_speech"
        phrases = CantonesePhrase.objects.all()
        #print(phrases)
        for phrase in phrases:
            payload = {
                "providers": "google",
                "language": "yue-HK",
                "option": "MALE",
                "text": phrase.text,
                "fallback_providers": ""
            }

            response = requests.post(url, json=payload, headers=headers)
            result = json.loads(response.text)
            audio_url = result["google"]["audio_resource_url"]
            audio_response = requests.get(audio_url)

            if audio_response.status_code == 200:
                filename = f"cantonese{phrase.number:02d}AI.mp3"
                self.save_audio(filename, audio_response.content)
                self.stdout.write(f"Audio file saved successfully for phrase {phrase.number}: {phrase.text}")
            else:
                self.stdout.write(f"Error downloading audio for phrase {phrase.number}: {audio_response.status_code}")

    def handle(self, *args, **kwargs):
        self.generate_audio_for_phrases()