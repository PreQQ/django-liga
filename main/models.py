from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Stadium(models.Model):
    name = models.CharField(max_length=50)
    localization = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    established = models.DateField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Player(models.Model):
    class PositionChoices(models.TextChoices):
        GK = 'GK'
        LB = 'LB'
        CB = 'CB'
        RB = 'RB'
        LM = 'LM'
        RM = 'RM'
        CM = 'CM'
        LS = 'LS'
        RS = 'RS'
        CS = 'CS'
        SUB = 'SUB'

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    shirt_number = models.IntegerField()
    birth_date = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=3, choices=PositionChoices.choices, default="SUB")

    def __str__(self):
        return self.first_name + " " + self.last_name

class Match(models.Model):
    host = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='host')
    guest = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='guest')
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    date = models.DateField()
    match_round = models.IntegerField()

    def __str__(self):
        return self.host.name + " - " + self.guest.name + " (kolejka: " + str(self.match_round) + ")" 

class Event(models.Model):
    class EventChoices(models.TextChoices):
        GOAL = 'GOAL', _('Gol')
        SHOT = 'SHOT', _('Strzał')
        FOUL = 'FOUL', _('Faul')
        YELLOW_CARD = 'YCAR', _('Żółta kartka')
        RED_CARD = 'RCAR', _('Czerwona kartka')
        PENALTY = 'PENL', _('Karny')
        PENALTY_GOAL = 'GPEN', _('Gol z karnego')
        OFFSIDE = 'OFFS', _('Spalony')
        CORNER = 'CRNR', _('Rożny')
        FREEKICK = 'FKCK', _('Wolny')
        ASSIST = 'ASST', _('Asysta')
    
    event_type = models.CharField(max_length=4, choices=EventChoices.choices)
    minute = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.match) + " (" + str(self.minute) + "') " + self.event_type

class Change(models.Model):
    in_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_in')
    out_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_out')
    minute = models.IntegerField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.match) + " (" + str(self.in_player.team) + " - " + str(self.in_player) + ")"