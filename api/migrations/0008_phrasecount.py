# Generated by Django 5.0.7 on 2024-08-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_game_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhraseCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
