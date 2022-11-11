from pydoc import describe
from django.db import models

class Event(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='events_organizer')
    description = models.CharField(max_length=155)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    gamers = models.ManyToManyField('Gamer', through='EventGamer')

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value