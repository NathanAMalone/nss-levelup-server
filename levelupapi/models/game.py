from django.db import models

class Game(models.Model):

    game_type = models.ForeignKey('GameType', on_delete=models.CASCADE)
    gamer = models.ForeignKey('Gamer', on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.PositiveIntegerField(null=True)
    skill_level = models.PositiveIntegerField(null=True)