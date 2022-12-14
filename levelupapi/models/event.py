from pydoc import describe
from django.db import models

from levelupapi.models.gamer import Gamer

class Event(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE)
    description = models.CharField(max_length=155)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    gamers = models.ManyToManyField(Gamer)
