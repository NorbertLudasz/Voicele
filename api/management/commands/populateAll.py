from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from api.models import (
    EnglishPhrase, CantonesePhrase, FrenchPhrase, GermanPhrase,
    GreekPhrase, HebrewPhrase, HungarianPhrase, JapanesePhrase,
    MandarinPhrase, RomanianPhrase, RussianPhrase, UkranianPhrase
)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        phrase_models = [
            EnglishPhrase, CantonesePhrase, FrenchPhrase, GermanPhrase,
            GreekPhrase, HebrewPhrase, HungarianPhrase, JapanesePhrase,
            MandarinPhrase, RomanianPhrase, RussianPhrase, UkranianPhrase
        ]

        for model in phrase_models:
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted all entries from {model.__name__}'))

        populate_commands = [
            'populateEnglish', 'populateFrench', 'populateGerman',
            'populateGreek', 'populateHebrew', 'populateHungarian',
            'populateJapanese', 'populateMandarin', 'populateRomanian',
            'populateRussian', 'populateUkranian'
        ]

        for command in populate_commands:
            try:
              call_command(command)
              self.stdout.write(self.style.SUCCESS(f'Running command successful: {command}'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'Error running command {command}: {e}'))