from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from API.models import Games
from API.models import Players
from API.models import Questions

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

# Create a game
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def CreateGame(request, numberOfRounds):
    # Create a new game object
    newGame = Games()

    # Add the number of rounds they want
    newGame.numberOfRounds = numberOfRounds

    # Add the status of 'notStarted'
    newGame.status = "notstarted"

    # Save the newGame in the database
    newGame.save()

    # Convert the id to hex
    gameCode = hex(newGame.gameID)

    return Response(gameCode)

# Start the game
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def StartGame(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so update the game to started
        game = Games.objects.get(gameID = gameID)
        game.status = 'started'
        game.save()

    return Response(gameCode)

# Get participants of the game
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def GetParticipants(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    playersArray = []

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so get all the players of that game
        players = Players.objects.filter(gameID = gameID)

        # Put the players in an array
        for player in players:
            playersArray.append(player.playerID)
            
    # Send back the array
    return Response(playersArray)

# Join a game
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
@permission_classes((permissions.AllowAny,))
def JoinGame(request, gameCode, clientName):
    # Check if the game exists
    # Convert the gameCode to an integer
    searchGameID = int(gameCode, 0)

    # Hit the database
    if Games.objects.filter(gameID=searchGameID):
        # The game is found
        # Add them to the players
        newPlayer = Players()
        newPlayer.gameID = Games.objects.filter(gameID=searchGameID)[0]
        newPlayer.realName = clientName
        newPlayer.numberOfPicks = 0
        newPlayer.points = 0
        newPlayer.save()

        return Response(newPlayer.playerID)
    else:
        # The game is not found
        return Response('That game does not exist.')

# Start the game
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def InputQuestion(request):
    question = request.data['question']

    # Input the question into the database
    newQuestion = Questions()
    newQuestion.question = question
    newQuestion.save()

    return Response(newQuestion.questionID)

#WebSockets
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, '/game/index.html')