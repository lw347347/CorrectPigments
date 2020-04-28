from django.shortcuts import render

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
        'gameCode': gameCode
    })

def JoinGame(request):
    return render(request, 'clientGame/JoinGame.html')

def GameClient(request, gameCode, clientName):
    return render(request, 'clientGame/GameClient.html', {
        'gameCode': gameCode,
        'clientName': clientName
    })