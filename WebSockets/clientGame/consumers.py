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

        # Grab all the players and their scores
        URL = 'http://0.0.0.0/API/GrabScores/' + self.room_name
        response = requests.get(url = URL)
        if (response):
            playersArray = response.json()
        else:
            x = 1
        # Send the message that so and so has entered
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'someoneJoined',
                'scores': playersArray
            }
        )

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
            URL = 'http://0.0.0.0/API/StartGame/' + self.room_name
            requests.get(url = URL)

            # Grab all the participants of that game
            URL = 'http://0.0.0.0/API/GetParticipants/' + self.room_name
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

            # Grab all the players and their scores (0)
            URL = 'http://0.0.0.0/API/GrabScores/' + self.room_name
            response = requests.get(url = URL)
            playersArray = response.json()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sendScores',
                    'scores': playersArray
                }
            )

            # Figure out who is picking the first question
            URL = 'http://0.0.0.0/API/PickAQuestion/' + self.room_name
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
            URL = 'http://0.0.0.0/API/InputGameQuestion/' + self.room_name + '/' + str(question['questionID']) + '/' + str(playerID)
            response = requests.get(url = URL)

            # Get names
            URL = 'http://0.0.0.0/API/GetParticipantNames/' + self.room_name
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
            URL = 'http://0.0.0.0/API/CastVote/' + self.room_name + '/' + str(voterID) + '/' + str(playerID1) + '/'
            response = requests.get(url = URL)

            # Call the API for the second vote
            URL = 'http://0.0.0.0/API/CastVote/' + self.room_name + '/' + str(voterID) + '/' + str(playerID2) + '/'
            response = requests.get(url = URL)

        # Check if it's time to make predictions
        elif ( message == 'makePrediction'):
            # Grab all the participants of that game
            URL = 'http://0.0.0.0/API/GetParticipants/' + self.room_name
            response = requests.get(url = URL)

            # This contains a list of players by their playerID
            playersArray = response.json()

            # Add the host to the players Array
            playersArray.append(-1)

            # Send the message to make prediction 
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'makePrediction',
                    'message': 'makePrediction',
                    'recipients': playersArray
                }
            )

        # Check if someone made a prediction
        elif ( message == 'someonePredicted' ):
            playerID = text_data_json['playerID']
            prediction = text_data_json['prediction']

            # Send the predictions to the API
            URL = 'http://0.0.0.0/API/MakePrediction/' + self.room_name + '/' + str(playerID) + '/' + prediction
            response = requests.get(url = URL)
            response = response.json()

            # Send the response to the gameHost
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'madePrediction',
                    'player': response['player'],
                    'votesPredicted': response['votesPredicted'],
                    'actualVotes': response['actualVotes'],
                    'pointsEarned': response['pointsEarned'],
                    'recipients': [-1]
                }
            )

        # Check if we are ready for the next round
        elif ( message == 'readyForNextRound' ):
            # Find out who's in charge of the game
            URL = 'http://0.0.0.0/API/WhoIsInCharge/' + self.room_name
            response = requests.get(url = URL)
            personInCharge = response.json()

            # Send the nextRound button to the person in charge of the game
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'nextRoundButton',
                    'recipients': personInCharge
                }
            )

        # Check if it's time for the next round
        elif ( message == 'nextRound' ):
            # Grab all the players and their scores
            URL = 'http://0.0.0.0/API/GrabScores/' + self.room_name
            response = requests.get(url = URL)
            playersArray = response.json()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sendScores',
                    'scores': playersArray
                }
            )

            # Hit the API
            URL = 'http://0.0.0.0/API/NextRound/' + self.room_name 
            response = requests.get(url = URL)
            response = response.json()

            if response == 'continueTheGame':
                # Determine who get's to pick the next question
                URL = 'http://0.0.0.0/API/PickAQuestion/' + self.room_name
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
            else:
                # End the game
                # Grab all the scores for the game
                URL = 'http://0.0.0.0/API/GrabScores/' + self.room_name
                response = requests.get(url = URL)
                playersArray = response.json()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'endTheGame',
                        'scores': playersArray
                    }
                )

    # Grab all the scores for the game
    def grabScores():
        URL = 'http://0.0.0.0/API/GrabScores/' + self.room_name
        response = requests.get(url = URL)
        response = response.json()
        return(response)

    # Someonejoined
    def someoneJoined(self, event):
        scores = event['scores']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'someoneJoined',
            'recipients': [-1],
            'scores': scores
        }))

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

    # Vote
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

    # Make prediciton
    def makePrediction(self, event):
        recipients = event['recipients']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'makePrediction',
            'recipients': recipients
        }))

    # Someone made a prediciton
    def madePrediction(self, event):
        player = event['player']
        votesPredicted = event['votesPredicted']
        actualVotes = event['actualVotes']
        pointsEarned = event['pointsEarned']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'madePrediction',
            'recipients': [-1],
            'player': player,
            'votesPredicted': votesPredicted,
            'actualVotes': actualVotes,
            'pointsEarned': pointsEarned
        }))

    # Send scores
    def nextRoundButton(self, event):
        recipients = event['recipients']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'nextRoundButton',
            'recipients': recipients
        }))

    # Send scores
    def sendScores(self, event):
        scores = event['scores']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'scores',
            'recipients': [-1],
            'scores': scores
        }))

    # End the game
    def endTheGame(self, event):
        scores = event['scores']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'endTheGame',
            'recipients': [-1],
            'scores': scores
        }))