from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from .serializers import GameSerializer, CreateGameSerializer, LoginSerializer, UserSerializer, UserStatsSerializer
from .models import Game
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from random import sample
import random
from django.db.models import Count, Avg, Q
from datetime import datetime
from django.utils import timezone

class GameView(generics.ListAPIView):
  queryset = Game.objects.all()
  serializer_class = GameSerializer

class CreateGameView(APIView):
    serializer_class = CreateGameSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        #print("Received creategame data:", request.data)
        serializer = self.serializer_class(data=request.data)
        #print("created creategame serializer")
        if serializer.is_valid():
            #print("serializer is valid")
            hintPerms = serializer.data.get('hintPerms')
            guessHintNum = serializer.data.get('guessHintNum')
            player = request.user

            seed_date = request.data.get('seed_date')
            #print("seed date from request.data.get: ", seed_date)
            if seed_date:
                try:
                    seed_date = datetime.strptime(seed_date, "%Y-%m-%d").date()
                    if (timezone.now().date() - seed_date).days > 7:
                        return Response({"error": "Seed date too old."}, status=status.HTTP_400_BAD_REQUEST)
                except ValueError:
                    return Response({"error": "Bad seed date format."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                seed_date = timezone.now().date()

            existing_game = Game.objects.filter(player=player, createdAt__date=seed_date).first()
            if existing_game:
                #print("Game with this date already exists:", existing_game)
                return Response({"error": "You've already played this date's game."}, status=status.HTTP_400_BAD_REQUEST)

            game = Game(player=player, hintPerms=hintPerms, guessHintNum=guessHintNum)
            #print("game variable declared")
            
            aware_seed_datetime = timezone.make_aware(datetime.combine(seed_date, datetime.min.time()))
            #print("Aware seed datetime:", aware_seed_datetime)
            game.createdAt = aware_seed_datetime
            game.save()

            #print("game created or updated with seed_date")
            return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        #print("Received register data:", request.data)
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            #print("Username: ", username)
            #print("Password: ", password)
            if not username or not password:
                return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
            #print("past 1st if")
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            #print("past 2nd if")
            user = User.objects.create_user(username=username, password=password)
            #print("past user creation")
            token = Token.objects.create(user=user)
            #print("token created: ", token.key)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, format=None):
        #print("Received login data:", request.data)
        serializer = LoginSerializer(data=request.data)
        #print("login seralizer created")
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            #print("got login username: ", username)
            #print("got login password: ", password)
            user = authenticate(request, username=username, password=password)
            #print("after user = authenticate")
            if user is not None:
                #print("right before final login")
                login(request, user)
                #print("right after final login")
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
                #return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            game = Game.objects.get(id=id)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=200)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=404)
        
class GameAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_id):
        try:
            #print("trying to get game with id: ", game_id)
            game = Game.objects.get(id=game_id)
            #print("got game: ", game)
            #print("game.player: ", game.player)
            #print("request.user: ", request.user)
            
            if game.player == request.user:
                return Response({
                    "authorized": True,
                    "phraseSound": game.phraseSound
                }, status=status.HTTP_200_OK)
            else:
                return Response({"authorized": False}, status=status.HTTP_403_FORBIDDEN)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

#@csrf_exempt        
class GuessView(APIView):
    #print("aaaaaaaaa")
    permission_classes = [IsAuthenticated]
    #print("bbbbbbbb")
    #@method_decorator(csrf_exempt)
    language_data = {
        "English": {
            "fun_fact": "English is the most widely spoken language in the whole world!",
            "hint": "If the voice clips sound completely different than the sounds of the latin letters, it might be English.",
            "family": "Germanic"
        },
        "Romanian": {
            "fun_fact": "Romanian is a language spoken primarily in Romania which privdes itself in being a romantic latin language in a sea of slavs.",
            "hint": "You can have an easier time guessing Romanian if you recognize certain groups of characters like ce, ci, che or chi.",
            "family": "Latin"
        },
        "Cantonese": {
            "fun_fact": "If you're speaking to someone online who knows Cantonese they're probably from Hong Kong as other areas which primarily speak it are in core China and they have internet censorship.",
            "hint": "In all honesty this is a hard language to diferrentiate from the other sino-tibetian ones but know when you see characters like the ones here, that it will be one of them, Cantonese included.",
            "family": "Sino-Tibetan"
        },
        "French": {
            "fun_fact": "French is known as the language of love. Also the british hate it.",
            "hint": "If you see lots of vowels and w sounds, it might be French.",
            "family": "Latin"
        },
        "German": {
            "fun_fact": "German is probably the most useful language to learn if you want to migrate to Western Europe.",
            "hint": "If it sounds like the speaker is angry or very serious, it might be German.",
            "family": "Germanic"
        },
        "Greek": {
            "fun_fact": "Greek ius one of the oldest languages still spoken to this day, though archaic greek differs greatly from modern greek.",
            "hint": "This language is primarily spoken in Greece and Cyprus and uses the Greek alphabet. No other language uses this alphabet so if you are able to recognize it you will guess correctly every time!",
            "family": "Indo-European"
        },
        "Hebrew": {
            "fun_fact": "Hebrew is the most important language for devout christians to learn.",
            "hint": "If you see many short box-like characters without too many squiggly lines, it might be Hebrew.",
            "family": "Afro-Asiatic"
        },
        "Hungarian": {
            "fun_fact": "Hungarian is a unique language with no close relatives in Europe, being a bit of an outcast.",
            "hint": "If you see right leaning accents from the middle of a letter often, it might be Hungarian.",
            "family": "Uralic"
        },
        "Japanese": {
            "fun_fact": "Japanese uses three different scripts: Kanji, Hiragana, and Katakana. The latter two are easier to learn.",
            "hint": "Compared to the Sino-Tibetian languages like Mandarin or Cantonese, Japanese also uses more simpler but unique character that might help you recognize it called Hiragana and Katakana.",
            "family": "Japonic"
        },
        "Mandarin": {
            "fun_fact": "Mandarin is the most spoken language in the world by the number of native speakers because China exists.",
            "hint": "If the characters seem unique, complex and condensed it's bound to be one of the sino-tibetian languages, Mandarin being the most widely spoken one.",
            "family": "Sino-Tibetan"
        },
        "Russian": {
            "fun_fact": "Russian is widely spoken by nearly all of Russia's surrounding countries due to its influence.",
            "hint": "If you see the cyrillic alphabet, it might not be a bad shout to guess Russian.",
            "family": "Slavic"
        },
        "Ukranian": {
            "fun_fact": "You don't want to call a Ukranian speaker a Russian.",
            "hint": "If you see the cyrillic alphabet, Ukranian might not be a bad guess.",
            "family": "Slavic"
        }
    }


    def post(self, request, game_id):
        #print("GuessView post method reached")
        #print("request.auth: ", request.auth)  # This should print the auth token
        #print("request.user: ", request.user)  # This should print the user object
        ##print("request.user: ", request.user)
        #print("makeguessview trying to get game")
        game = get_object_or_404(Game, id=game_id)
        fun_fact = self.language_data[game.lang]["fun_fact"]
        language_hint = self.language_data[game.lang]["hint"]
        language_family = self.language_data[game.lang]["family"]

        #print("makeguessview got game: ", game)
        if game.player != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        #print("incrementing guessNum")
        game.guessNum += 1

        if game.gameStatus == 2:
            return Response({
                "result": "You have already won! You cannot make more guesses.",
                "gameStatus": game.gameStatus,
                "funFact": fun_fact
            })
        elif game.gameStatus == 0:
            return Response({
                "result": "You have already lost! You cannot make any more guesses.",
                "gameStatus": game.gameStatus,
                "languageHint": language_hint
            })
        
        selected_language = request.data.get('selected_language')
        #print("selected language: ", selected_language)
        #print("game lang: ", game.lang)

        if selected_language == game.lang:
            game.gameStatus = 2
            game.save()
            return Response({
                "result": "Correct Guess! You win!",
                "gameStatus": game.gameStatus,
                "funFact": fun_fact
            })

        if game.guessNum >= 6:
            game.gameStatus = 0
            game.save()
            return Response({
                "result": "Game Over! You lost...",
                "gameStatus": game.gameStatus,
                "languageHint": language_hint})

        game.save()
        #print("incremented and saved guessNum")

        #print("game.guessNum, game.guessHintNum, game.hintPerms: ", game.guessNum, game.guessHintNum, game.hintPerms)
        if game.guessNum == game.guessHintNum and game.hintPerms:
            #return Response({"result": "Wrong Guess. Hints enabled!"})
            all_languages = ["English", "Romanian", "Hungarian", "German", "Russian", "Ukrainian", 
                             "Greek", "Japanese", "Mandarin", "Cantonese", "Hebrew", "French"]
            other_languages = sample([lang for lang in all_languages if lang != game.lang], 3)
            multiple_choice_hint = other_languages + [game.lang]
            random.shuffle(multiple_choice_hint)
            
            return Response({
                "result": "Wrong Guess. Hints enabled!",
                "hint1": game.phrase,
                "hint2": multiple_choice_hint,
                "hint3": language_family,
                "gameStatus": game.gameStatus
            })

        return Response({
            "result": "Wrong Guess. Try again.",
            "gameStatus": game.gameStatus
        })
    
class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        games_played = Game.objects.filter(player=user).count()

        games_won = Game.objects.filter(player=user, gameStatus=2).count()

        games_lost = Game.objects.filter(player=user, gameStatus=0).count()

        average_guesses_to_win = Game.objects.filter(player=user, gameStatus=2).aggregate(Avg('guessNum'))['guessNum__avg']
        average_guesses_to_win = round(average_guesses_to_win, 2) if average_guesses_to_win else 0.0

        streak = 0
        current_date = timezone.now().date()

        while True:
            if Game.objects.filter(player=user, gameStatus=2, createdAt__date=current_date).exists():
                streak += 1
                current_date = current_date - timezone.timedelta(days=1)
            else:
                break
        #print("streak: ", streak)

        language_stats = {}
        games_by_language = Game.objects.filter(player=user).exclude(gameStatus=1).values('lang').annotate(
            total_games=Count('id'),
            wins=Count('id', filter=Q(gameStatus=2)),
            losses=Count('id', filter=Q(gameStatus=0))
        )

        for game in games_by_language:
            language = game['lang']
            total_games = game['total_games']
            wins = game['wins']
            success_rate = round((wins / total_games) * 100, 2)
            language_stats[language] = success_rate

        stats = {
            "games_played": games_played,
            "games_won": games_won,
            "games_lost": games_lost,
            "average_guesses_to_win": average_guesses_to_win,
            "language_stats": language_stats,
            "daily_streak": streak,
        }

        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
    
class PastGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        player = request.user
        games = Game.objects.filter(player=player)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)