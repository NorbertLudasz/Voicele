from django.core.management.base import BaseCommand
from api.models import CantonesePhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "剩返最後一句, 我應該講啲乜嘢呢?",
            "你食咗飯未?",
            "班房入面好嘈啊..",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            CantonesePhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'cantonese{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} CantonesePhrase entries'))