from django.core.management.base import BaseCommand
from api.models import EnglishPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        # Sample texts for the phrases 1st object=number 2nd text, 2nd-3rd, 3rd-1st
        sample_texts = [
            "Excuse me, but you wouldn't happen to have the time on you right now, would you?",
            "Hi! It's been so long, how have you been?",
            "I'm truly grateful for all your help.",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            EnglishPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'english{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} EnglishPhrase entries'))