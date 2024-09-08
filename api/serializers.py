from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game

class GameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Game
    fields = ('id', 'lang', 'phraseID', 'phrase', 'phraseSound', 'hintPerms', 'guessNum', 'guessHintNum', 'createdAt', 'player', 'gameStatus')

class CreateGameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Game
    #fields = ('lang', 'phraseID')
    fields = ('hintPerms', 'guessHintNum')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserStatsSerializer(serializers.Serializer):
    games_played = serializers.IntegerField()
    games_won = serializers.IntegerField()
    games_lost = serializers.IntegerField()
    average_guesses_to_win = serializers.FloatField()
    language_stats = serializers.DictField(
        child=serializers.FloatField(),
        default=dict
    )
    daily_streak = serializers.IntegerField()