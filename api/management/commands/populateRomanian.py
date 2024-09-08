from django.core.management.base import BaseCommand
from api.models import RomanianPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "Vrei să mâncăm niște clătite?",
            "Ce crezi de noul profesor?",
            "Am cumpărat o vază nouă pentru florile mele",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            RomanianPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'romanian{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} RomanianPhrase entries'))