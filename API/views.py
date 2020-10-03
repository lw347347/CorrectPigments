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
from API.models import Votes

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

# Get who is in charge
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def WhoIsInCharge(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    playersArray = []

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so get all the players of that game
        players = Players.objects.filter(gameID = gameID)

        # Put the players in an array
        iCount = 0
        for player in players:
            if (iCount == 0):
                playersArray.append(player.playerID)
            iCount = iCount + 1
            
    # Send back the one who's in charge
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
        # Check if they are already in the game
        if Players.objects.filter(gameID=searchGameID, realName=clientName).exists():
            # They already are in the game so send back the right player id
            player = Players.objects.filter(gameID=searchGameID, realName=clientName).values()[0]
            return Response(player['playerID'])

        else:
            # They aren't in the game yet        
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
        lowestNumberOfPicks = 1000
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
        randomNumber = round(random() * len(playersArray)) - 1
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
        randomNumber1 = round(random() * len(questions)) - 1
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

        # Increment the numberOfPicks on the random player
        randomPlayerDatabase = Players.objects.filter(playerID = randomPlayer['playerID'])[0]
        randomPlayerDatabase.numberOfPicks = randomPlayerDatabase.numberOfPicks + 1
        randomPlayerDatabase.save()

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

# Cast Vote
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def CastVote(request, gameCode, voterID, playerID):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so get the players we're looking for
        voter = Players.objects.filter(playerID = voterID)[0]
        player = Players.objects.filter(playerID = playerID)[0]

        # Find the gameQuestion we're looking for
        gameQuestion = GameQuestions()
        gameQuestions = GameQuestions.objects.filter(gameID = gameID)
        for question in gameQuestions:
            gameQuestion = question

        # Input everything into the database
        vote = Votes()
        vote.gameQuestionID = gameQuestion
        vote.voterID = voter
        vote.playerID = player
        vote.save()

    # Send back the voteID
    return Response(vote.voteID)

# Make Prediction
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def MakePrediction(request, gameCode, playerID, prediction):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)
    
    # Make the playerID an int
    playerID = int(playerID)

    # Find out if they have most, some, or none of the votes
    # Get the last gameQuestionID
    gameQuestionID = ''
    gameQuestions = GameQuestions.objects.filter(gameID = gameID)
    for question in gameQuestions:
        gameQuestionID = question.gameQuestionID

    # Get the votes for that gameQuestion
    votes = Votes.objects.filter(gameQuestionID = gameQuestionID)

    # Tally up the votes
    voteArray = []
    for vote in votes:
        # Check if that player is in the voteArray
        theyAreInAlready = False
        voteArrayIndex = 0
        for item in voteArray:
            if vote.playerID == item[0]:
                theyAreInAlready = True
                break
            else:
                voteArrayIndex = voteArrayIndex + 1
        if theyAreInAlready == True:
            # Increment how many votes they have
            voteArray[voteArrayIndex][1] = voteArray[voteArrayIndex][1] + 1
        else:
            # They aren't in there so push them to it and increment their vote count
            voteArray.append([vote.playerID, 1])
    # Determine the highest number of votes
    highestNumberOfVotes = 0
    numberOfVotesForPlayer = 0
    for vote in voteArray:
        if vote[1] > highestNumberOfVotes:
            highestNumberOfVotes = vote[1]
        if vote[0].playerID == playerID:
            # Determine how many votes they received
            numberOfVotesForPlayer = vote[1]

    # Determine if they had most, some, or none
    correctPrediction = ''
    if numberOfVotesForPlayer == 0:
        correctPrediction = 'none'
    elif numberOfVotesForPlayer < highestNumberOfVotes:
        correctPrediction = 'some'
    else:
        correctPrediction = 'most'
    
    # Determine how many points they get
    pointsEarned = 0
    if prediction == correctPrediction:
        if prediction == 'some':
            # They get 1 point
            player = Players.objects.filter(playerID = playerID)[0]
            player.points = player.points + 1
            player.save()
            pointsEarned = 1

        elif prediction == 'most':
            # They get 3 points
            player = Players.objects.filter(playerID = playerID)[0]
            player.points = player.points + 3
            player.save()
            pointsEarned = 3

        elif prediction == 'none':
            # They get 3 points
            player = Players.objects.filter(playerID = playerID)[0]
            player.points = player.points + 3
            player.save()
            pointsEarned = 3

    else:
        # They get zero points
        pointsEarned = 0
    
    player = Players.objects.filter(playerID = playerID)[0]
    player = player.realName
    votesPredicted = prediction
    actualVotes = numberOfVotesForPlayer

    response = { 
        'player': player,
        'votesPredicted': votesPredicted,
        'actualVotes': actualVotes,
        'pointsEarned': pointsEarned
    }


    # Send back the response
    return Response(response)

# Next Round
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def NextRound(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so count the numberOfRounds
        numberOfRounds = 0
        gameQuestions = GameQuestions.objects.filter(gameID = gameID)
        for item in gameQuestions:
            numberOfRounds = numberOfRounds + 1
        
        # Compare that to the number of rounds in the game
        game = Games.objects.filter(gameID = gameID)[0]
        if numberOfRounds < game.numberOfRounds:
            # The game should continue
            return Response('continueTheGame')
        else:
            # The game should end
            return Response('endTheGame')

    # Send back the voteID
    return Response(vote.voteID)

# Grab Scores
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def GrabScores(request, gameCode):
    # Convert the gameCode to int
    gameID = int(gameCode, 0)
    
    playersArray = []

    # Find the game
    if Games.objects.filter(gameID = gameID):
        # It's found so grab all the players
        players = Players.objects.filter(gameID = gameID).order_by('-points')
        for player in players:
            playersArray.append({ 'realName': player.realName, 'points': player.points })

    # Send back the voteID
    return Response(playersArray)

#WebSockets
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, '/game/index.html')