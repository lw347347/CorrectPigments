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
            

        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        recipients = event['recipients']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'recipients': recipients
        }))