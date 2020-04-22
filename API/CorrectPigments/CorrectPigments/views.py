from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from CorrectPigments.serializers import UserSerializer
from rest_framework.decorators import api_view
from CorrectPigments.models import Games
from CorrectPigments.models import Players

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create a game
@api_view(http_method_names=['GET'])
def CreateGame(request):
    # Create a new game object
    newGame = Games()

    # Add the number of rounds they want
    newGame.numberOfRounds = request.query_params.get('numberOfRounds')

    # Add the status of 'notStarted'
    newGame.status = "notstarted"

    # Save the newGame in the database
    newGame.save()

    # Convert the id to hex
    gameCode = hex(newGame.gameID)

    return gameCode

# Join a game
@api_view(http_method_names=['GET'])
def JoinGame(request):
    # Check if the game exists
    # Convert the gameCode to an integer
    searchGameID = int(request.query_params.get('gameCode'), 0)

    # Hit the database
    if Games.object.filter(gameID=searchGameID):
        # The game is found
        # Add them to the players
        newPlayer = Players()
        newPlayer.gameID = searchGameID
        newPlayer.realName = request.query_params.get('realName')
        newPlayer.nickname = request.query_params.get('nickname')
        newPlayer.numberOfPicks = 0
        newPlayer.points = 0
        newPlayer.save()

        return searchGameID
    else:
        # The game is not found
        return ('That game does not exist.')