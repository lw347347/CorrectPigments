from django.db import models

class Games(models.Model):
    gameID = models.AutoField(primary_key=True)
    numberOfRounds = models.IntegerField()

class Players(models.Model):
    playerID = models.AutoField(primary_key=True)
    gameID = models.ForeignKey(Games, on_delete=models.CASCADE)
    realName = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    numberOfPicks = models.IntegerField()
    points = models.IntegerField()

class Questions(models.Model):
    questionID = models.AutoField(primary_key=True)
    question = models.CharField(max_length=9999)

class GameQuestions(models.Model):
    gameQuestionID = models.AutoField(primary_key=True)
    questionID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    # This is to keep track of who chose the question
    playerID = models.ForeignKey(Players, on_delete=models.CASCADE)
    gameID = models.ForeignKey(Games, on_delete=models.CASCADE)
    roundNumber = models.IntegerField()

class Votes(models.Model):
    voteID = models.AutoField(primary_key=True)
    gameQuestionID = models.ForeignKey(GameQuestions, on_delete=models.CASCADE)
    # This is for the person who is voting
    voterID = models.ForeignKey(Players, related_name='voterID_FK', on_delete=models.CASCADE)
    # This is the person who is getting voted for
    playerID = models.ForeignKey(Players, related_name='playerID_FK', on_delete=models.CASCADE)

