from django.core.management.base import BaseCommand
from api.models import GreekPhrase

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_phrases = 3

        sample_texts = [
            "Πάνω από κάθε προσδοκία μου, ένας πόνος ανένδωτος μένει μέσα στην καρδιά μου",
            "Αρχή μιας ζωής από το μηδέν σε έναν άλλο κόσμο",
            "Δώσε μου λόγο να σε εμπιστευτώ",
        ]

        if len(sample_texts) < num_phrases:
            sample_texts *= (num_phrases // len(sample_texts)) + 1

        for i in range(1, num_phrases + 1):
            GreekPhrase.objects.create(
                number=i,
                text=sample_texts[i % len(sample_texts)],
                mp3_file=f'greek{i:02d}.mp3'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_phrases} GreekPhrase entries'))