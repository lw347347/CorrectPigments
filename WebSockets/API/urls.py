from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CreateGame/<int:numberOfRounds>', views.CreateGame, name='CreateGame'),
    path('StartGame/<str:gameCode>', views.StartGame, name='StartGame'),
    path('JoinGame/<str:gameCode>/<str:clientName>/', views.JoinGame, name='JoinGame'),
    path('GetParticipants/<str:gameCode>/', views.GetParticipants, name='GetParticipants'),
    path('InputQuestion/', views.InputQuestion, name='InputQuestion'),
    path('PickAQuestion/<str:gameCode>/', views.PickAQuestion, name='PickAQuestion'),
    path('GetParticipantNames/<str:gameCode>/', views.GetParticipantNames, name='GetParticipantNames'),
    path('InputGameQuestion/<str:gameCode>/<int:questionID>/<int:playerID>/', views.InputGameQuestion, name='InputGameQuestion'),
    path('', views.index, name='index'),
]