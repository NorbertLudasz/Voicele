from django.core.management.base import BaseCommand
from api.models import JapanesePhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "わたしは にほんごがすこししか はなせません",
            "はじめまして！ わたしのなまえは ‥‥です",
            "これはいくらですか ?",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            JapanesePhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'japanese{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} JapanesePhrase entries'))