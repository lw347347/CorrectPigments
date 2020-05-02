from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Max
from API.models import Games
from API.models import Players
from API.models import Questions
from API.models import GameQuestions

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

# Pick a person to pick the question and the questions they can pick from
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
@permission_classes((permissions.AllowAny,))
def PickAQuestion(request, gameCode):
    # Check if the game exists
    # Convert the gameCode to an integer
    searchGameID = int(gameCode, 0)

    # Hit the database
    if Games.objects.filter(gameID=searchGameID):
        # The game is found
        # Figure out the person who is picking the questions
        # Grab all the players from that game
        players = Players.objects.filter(gameID = searchGameID)
        lowestNumberOfPicks = 0
        playersArray = []

        # Figure out the lowest number of picks
        for player in players:
            if player.numberOfPicks < lowestNumberOfPicks:
                lowestNumberOfPicks = player.numberOfPicks

        # Add the players with the lowest number of picks
        for player in players:
            if player.numberOfPicks == lowestNumberOfPicks:
                playersArray.append(player)
        
        # Pick a random player
        from random import seed, random
        seed(12345)
        randomNumber = int(random() * len(playersArray)) - 1
        if randomNumber < 0:
            randomNumber = 0
        randomPlayer = {
            'playerID': playersArray[randomNumber].playerID,
            'realName': playersArray[randomNumber].realName
        }

        # Pick two random questions 
        # Grab all the questions that have been asked
        gameQuestions = (GameQuestions.objects.filter(gameID = searchGameID).values('questionID'))
        gameQuestionsArray = []
        for gameQuestion in gameQuestions:
            gameQuestionsArray.append(gameQuestion)

        # Filter the questions down by the gameQuestions
        # Grab all questions
        questions = Questions.objects.exclude(questionID__in=gameQuestions)
        questionsArray = []
        for question in questions:
            questionsArray.append({ 
                'questionID': question.questionID, 
                'question': question.question 
            })

        # Pick two random questions
        randomNumber1 = int(random() * len(questions)) - 1
        if randomNumber1 < 0:
            randomNumber1 = 0
        randomNumber2 = randomNumber1
        randomQuestion1 = questionsArray[randomNumber1]
        randomQuestion2 = questionsArray[0]
        while randomNumber1 == randomNumber2:
            randomNumber2 = int(random() * len(questionsArray)) - 1
            if randomNumber2 < 0:
                randomNumber2 = 0
        
        randomQuestion2 = questionsArray[randomNumber2]

        return Response({ 
            'playerID': randomPlayer, 
            'randomQuestion1': randomQuestion1, 
            'randomQuestion2': randomQuestion2 
        })
    else:
        # The game is not found
        return Response('That game does not exist.')

# Input Question
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def InputQuestion(request):
    question = request.data['question']

    # Input the question into the database
    newQuestion = Questions()
    newQuestion.question = question
    newQuestion.save()

    return Response(newQuestion.questionID)

# Input GameQuestion
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def InputGameQuestion(request, gameCode, questionID, playerID):
    # Create the game question
    gameQuestion = GameQuestions()

    # Convert the gamecode to the gameID
    gameID = int(gameCode, 0)

    # get the game, question, and player
    game = Games.objects.filter(gameID = gameID)[0]
    question = Questions.objects.filter(questionID = int(questionID))[0]
    player = Players.objects.filter(playerID = int(playerID))[0]
    
    # Get the roundNumber
    gameQuestions = GameQuestions.objects.filter(gameID = gameID)
    roundNumber = 1
    for item in gameQuestions:
        roundNumber = roundNumber + 1

    # Put the gameID, questionID, playerID, and roundNumber
    gameQuestion.gameID = game
    gameQuestion.questionID = question
    gameQuestion.playerID = player
    gameQuestion.roundNumber = roundNumber

    # Input the gamequestion into the database
    gameQuestion.save()

    return Response(gameQuestion.gameQuestionID)

# Get participant names
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def GetParticipantNames(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    playersArray = []

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so get all the players of that game
        players = Players.objects.filter(gameID = gameID)

        # Put the players in an array
        for player in players:
            playersArray.append({ 'playerID': player.playerID, 'realName': player.realName })
            
    # Send back the array
    return Response(playersArray)


#WebSockets
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, '/game/index.html')