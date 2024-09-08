from django.core.management.base import BaseCommand
from api.models import RussianPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "В нашем языке Санта Клауса называют Дед Мороз",
            "Карл у Клары украл кораллы, Клара у Карла украла кларнет",
            "Брест получил Магдебургское право в тысяча трёхсот девяностом году",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            RussianPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'russian{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} RussianPhrase entries'))