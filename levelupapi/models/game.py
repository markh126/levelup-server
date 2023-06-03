from django.db import models
from .game_type import GameType
from .gamer import Gamer


class Game(models.Model):

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()

    # @property
    # def event_info(self):
    #     """Event specific info"""
    #     return [event.description for event in self.events.all()]

    @property
    def event_info(self):
        """Event specific info"""
        info = []
        for event in self.events.all():
            info.append(event.description)
            info.append(event.date)
            info.append(event.time)
        return info
