import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import requests

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        playersArray = []

        # Check if it says to start the game
        if (message == 'startGame'):
            # Set the game as started in the API
            URL = 'http://192.168.1.38:8000/API/StartGame/' + self.room_name
            requests.get(url = URL)

            # Grab all the participants of that game
            URL = 'http://192.168.1.38:8000/API/GetParticipants/' + self.room_name
            response = requests.get(url = URL)

            # This contains a list of players by their playerID
            playersArray = response.json()

            # Add the host to the players Array
            playersArray.append(-1)

            # Send startGame message
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': 'The game has started.',
                    'recipients': playersArray
                }
            )

            # Figure out who is picking the first question
            URL = 'http://192.168.1.38:8000/API/PickAQuestion/' + self.room_name
            response = requests.get(url = URL)

            response = response.json()

            # Send the message to pick a question to the correct recipient
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'pick_question',
                    'randomQuestion1': response['randomQuestion1'],
                    'randomQuestion2': response['randomQuestion2'],
                    'recipients': [response['playerID'], '-1', response['playerID']['playerID']]
                }
            ) 
        elif ( message == "someonePickedAQuestion"):
            # Someone just picked a question
            # Grab the question and player
            question =  text_data_json['question']
            playerID =  text_data_json['playerID']

            # Input the gameQuestion into the database
            URL = 'http://192.168.1.38:8000/API/InputGameQuestion/' + self.room_name + '/' + str(question['questionID']) + '/' + str(playerID)
            response = requests.get(url = URL)

            # Get names
            URL = 'http://192.168.1.38:8000/API/GetParticipantNames/' + self.room_name
            response = requests.get(url = URL)

            # This is equal to all the playerIDs and their names
            names = response.json()
            recipients = []
            for recipient in names:
                recipients.append(recipient['playerID'])
            
            # Add the host onto the recipients
            recipients.append(-1)

            # Send the message to vote 
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'vote',
                    'question': question,
                    'recipients': recipients,
                    'names': names
                }
            )
        # Check if someone voted
        elif ( message == 'someoneVoted'):
            voterID =  text_data_json['voterID']
            playerID1 = text_data_json['votes']['playerID1']
            playerID2 = text_data_json['votes']['playerID2']
            # Call the API for the first vote
            URL = 'http://192.168.1.38:8000/API/CastVote/' + self.room_name + '/' + str(voterID) + '/' + str(playerID1) + '/'
            response = requests.get(url = URL)

            # Call the API for the second vote
            URL = 'http://192.168.1.38:8000/API/CastVote/' + self.room_name + '/' + str(voterID) + '/' + str(playerID2) + '/'
            response = requests.get(url = URL)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        recipients = event['recipients']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'recipients': recipients
        }))

    # Pick Question
    def pick_question(self, event):
        randomQuestion1 = event['randomQuestion1']
        randomQuestion2 = event['randomQuestion2']
        recipients = event['recipients']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'pick_question',
            'randomQuestion1': randomQuestion1,
            'randomQuestion2': randomQuestion2,
            'recipients': recipients
        }))

    # Pick Question
    def vote(self, event):
        question = event['question']
        recipients = event['recipients']
        names = event['names']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'Vote please',
            'question': question,
            'recipients': recipients,            
            'names': names,
        }))