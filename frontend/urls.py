from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('stats', index),
    path('pastgames', index),
    path('creategame', index),
    path('register', index),
    path('login', index),
    path('play/<int:id>/', index),
]
