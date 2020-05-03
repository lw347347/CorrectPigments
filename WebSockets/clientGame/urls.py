from django.urls import path

from . import views

urlpatterns = [
    path('InputQuestion/', views.InputQuestion, name='InputQuestion'),
    path('JoinGame/', views.JoinGame, name='JoinGame'),
    path('CreateGame/', views.CreateGame, name='CreateGame'),
    path('<str:room_name>/', views.room, name='room'),
    path('GameHost/<str:gameCode>/', views.GameHost, name='GameHost'),  
    path('GameClient/<str:gameCode>/<str:clientName>/', views.GameClient, name='GameClient'),    
    path('', views.JoinGame, name='JoinGame'),
    
]