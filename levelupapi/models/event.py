from django.db import models
from .game import Game
from .gamer import Gamer


class Event(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)

    @property
    def joined(self):
        """Join"""
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
