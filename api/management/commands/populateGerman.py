from django.core.management.base import BaseCommand
from api.models import GermanPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "Zehn zahme Ziegen zogen zehn Zentner Zucker zum Zoo",
            "Ich war bis vor einer Woche im Urlaub in Schweden",
            "In meiner Freizeit gehe ich sehr gerne Bouldern",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            GermanPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'german{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} GermanPhrase entries'))