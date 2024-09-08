from django.contrib import admin
from .models import EnglishPhrase

@admin.register(EnglishPhrase)
class EnglishPhraseAdmin(admin.ModelAdmin):
    list_display = ('number', 'text', 'mp3_file')
