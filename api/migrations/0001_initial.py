# Generated by Django 5.0.7 on 2024-07-18 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishPhrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('text', models.CharField(max_length=255)),
                ('mp3_file', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(default='', max_length=50, unique=True)),
                ('phraseID', models.IntegerField(default=0)),
                ('phrase', models.CharField(blank=True, default='', max_length=100)),
                ('phraseSound', models.CharField(blank=True, default='', max_length=100)),
                ('hintPerms', models.BooleanField(default=False)),
                ('guessNum', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
