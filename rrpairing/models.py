# -*- coding: utf-8 -*-
from django.db import models


class Team_tournament(models.Model):
    name = models.CharField(max_length=100)
    pairing_done = False
    def __unicode__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Team_tournament)

    def __unicode__(self):
        return self.name

    def count_points(self):
        w_games = self.white.all()
        b_games = self.black.all()
        points = 0
        for game in w_games:
            points += game.white_result
        for game in b_games:
            points += game.black_result
        return points

class Player(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    ELO = models.IntegerField(default=1600)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return self.name + " " + self.surname


class Round(models.Model):
    tournament = models.ForeignKey(Team_tournament)
    number = models.IntegerField(default=0)
    played = models.BooleanField(default=False)

    def __unicode__(self):
        return self.tournament.name + ", round " + str(self.number)

class Team_game(models.Model):
    round = models.ForeignKey(Round)
    white_team = models.ForeignKey(Team,related_name="white")
    black_team = models.ForeignKey(Team,related_name="black")
    white_result = models.FloatField(default=0)
    black_result = models.FloatField(default=0)

    def __unicode__(self):
        return self.white_team.name + " " + str(self.white_result) + ":" + str(self.black_result) + " " + self.black_team.name
