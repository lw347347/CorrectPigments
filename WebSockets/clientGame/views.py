from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, 'clientGame/index.html')

def room(request, room_name):
    return render(request, 'clientGame/room.html', {
        'room_name': room_name
    })

def CreateGame(request):
    return render(request, 'clientGame/CreateGame.html')

def GameHost(request, gameCode):
    return render(request, 'clientGame/GameHost.html', {
        'gameCode': gameCode,
        
    })

def JoinGame(request):
    return render(request, 'clientGame/JoinGame.html')

def GameClient(request, gameCode, clientName):
    # Add the client to the database in the API
    URL = 'http://869e7338.ngrok.io/API/JoinGame/' + gameCode + '/' + clientName
    response = requests.get(url = URL)
    print(response)

    return render(request, 'clientGame/GameClient.html', {
        'gameCode': gameCode,
        'clientName': clientName,
        'playerID': response.json()
    })

def InputQuestion(request):    
    return render(request, 'clientGame/InputQuestion.html')