from django.urls import path
from .views import GameView, CreateGameView, RegisterView, LoginView, GameDetailView, GameAuthView, GuessView, UserStatsView, PastGamesView, CurrentUserView

urlpatterns = [
    path('game/<int:id>/', GameDetailView.as_view()),
    path('gameauth/<int:game_id>/', GameAuthView.as_view()),
    path('guess/<int:game_id>/', GuessView.as_view()),
    path('past-games/', PastGamesView.as_view()),
    path('stats/', UserStatsView.as_view()),
    path('game', GameView.as_view()),
    path('create-game/', CreateGameView.as_view()),
    path('currentuser/', CurrentUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

]
