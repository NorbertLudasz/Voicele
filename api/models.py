from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

class PhraseCount(models.Model):
    language = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.language}: {self.count}"

class EnglishPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"

class CantonesePhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class FrenchPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class GermanPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class GreekPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class HebrewPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class HungarianPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class JapanesePhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class MandarinPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class RomanianPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class RussianPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class UkranianPhrase(models.Model):
  number = models.IntegerField(unique=True)
  text = models.CharField(max_length=255)
  mp3_file = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.number}: {self.text}"
  
class Game(models.Model):
  lang = models.CharField(max_length=50, default="")
  phraseID = models.IntegerField(null=False, default=0)
  phrase = models.CharField(max_length=100, default="")
  phraseSound = models.CharField(max_length=100, default="")
  hintPerms = models.BooleanField(null=False, default=False) #False means never hints, True means hints after guessHintNum wrong guesses, sent with post req
  guessNum = models.IntegerField(null=False, default=0)
  guessHintNum = models.IntegerField(null=False, default=3)
  createdAt = models.DateTimeField()
  player = models.ForeignKey(User, on_delete=models.CASCADE)
  gameStatus = models.IntegerField(null=False, default=1)
  LANGUAGES = [
      'English',
      'Romanian',
      'Hungarian',
      'German',
      'Russian',
      'Ukranian',
      'Greek',
      'Japanese',
      'Mandarin',
      'Cantonese',
      'Hebrew',
      'French',
    ]
  
  PHRASES_COUNT = {
      'English': 3,
      'Romanian': 3,
      'Hungarian': 3,
      'German': 3,
      'Russian': 3,
      'Ukranian': 3,
      'Greek': 3,
      'Japanese': 3,
      'Mandarin': 3,
      'Cantonese': 3,
      'Hebrew': 3,
      'French': 3
    }
  
  def setGame(self, seed_date=None):
        if seed_date is None:
            seed_date = timezone.now().date()

        random.seed(seed_date.toordinal())

        chosenLang = random.choice(self.LANGUAGES)
        self.lang = chosenLang

        maxPhraseNum = self.PHRASES_COUNT[chosenLang]

        phraseNum = random.randint(1, maxPhraseNum)
        self.phraseID = phraseNum

        phrase_entry = None
        phrase_model = {
            'English': EnglishPhrase,
            'Cantonese': CantonesePhrase,
            'French': FrenchPhrase,
            'German': GermanPhrase,
            'Greek': GreekPhrase,
            'Hebrew': HebrewPhrase,
            'Hungarian': HungarianPhrase,
            'Japanese': JapanesePhrase,
            'Mandarin': MandarinPhrase,
            'Romanian': RomanianPhrase,
            'Russian': RussianPhrase,
            'Ukranian': UkranianPhrase
        }.get(self.lang)

        if phrase_model:
            phrase_entry = phrase_model.objects.filter(number=self.phraseID).first()

        if phrase_entry:
            self.phrase = phrase_entry.text
            self.phraseSound = phrase_entry.mp3_file

  def save(self, *args, **kwargs):
        if not self.pk:
            super(Game, self).save(*args, **kwargs)
            self.setGame(seed_date=self.createdAt.date() if self.createdAt else None)
        super(Game, self).save(*args, **kwargs)

