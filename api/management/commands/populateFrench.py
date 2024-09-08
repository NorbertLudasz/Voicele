from django.core.management.base import BaseCommand
from api.models import FrenchPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "Et enfin j’adore apprendre de nouvelles langues et de découvrir de nouvelles cultures.",
            "Bonjour, je m’appelle Manh Hung, aka MomoNagi et je viens du Vietnam.",
            "Je suis actuellement un étudiant en quatrième année en école d’ingénieur spécialité informatique.",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            FrenchPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'french{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} FrenchPhrase entries'))