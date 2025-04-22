from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=256)
    link = models.CharField(max_length=1024, blank = True)
    pic_link = models.CharField(max_length=1024)

    
    def __str__(self):
        return f"{self.name}"    

class Event(models.Model):
    def __str__(self):
        return f"{self.name}"
    
    name = models.CharField(max_length=256)
    custom_pic_link = models.CharField(max_length=1024,blank = True)
    event_time = models.CharField(max_length=1024) # long description is more usefull.
    event_date = models.DateField()
    players = models.ManyToManyField(Player, through= 'EventPlayers')

class PastEvents(models.Model):
   pass

class EventPlayers(models.Model):
    def __str__(self):
        return f"{self.player} - {self.event}"
    
    player = models.ForeignKey(Player,on_delete=models.SET_NULL, null = True)
    event  = models.ForeignKey(Event,on_delete=models.SET_NULL, null = True)


class Game(models.Model):
    def __str__(self):
        return f"{self.name}"
    
    name = models.CharField(max_length=256)
    link = models.CharField(max_length=1024, blank= True)
    extra_text = models.CharField(max_length=256, blank = True)
    extra_link = models.CharField(max_length=1024,blank = True)

class GameInstance(models.Model):

    def __str__(self):
        return f"{self.game} @ { self.event}"
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null = True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null = True)
    score = models.ManyToManyField(Player, through= 'Scores')
    hiden = models.BooleanField()
                                   
class Scores(models.Model):
    def __str__(self):
        return f"{self.game_instance} : - {self.player} - {self.score}"
    game_instance = models.ForeignKey(GameInstance,on_delete=models.CASCADE, null= True) # never delete bro
    player = models.ForeignKey(Player,on_delete=models.SET_NULL, null = True) # never delete bro
    score = models.IntegerField()

class PrevEventLink(models.Model):
    name = models.CharField(max_length=1024)
    link = models.CharField(max_length=1024)