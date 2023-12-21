from django.db import models
from django.contrib.auth.models import User


class Position(models.Model):
    name = models.CharField(max_length=50, primary_key=True, verbose_name="name position",
                            help_text="Input the name of position", null=False, blank=False)
    name_coach = models.CharField(max_length=100)

    def __str__(self):
        return "Position: " + self.name

class Club(models.Model):
    name = models.CharField(max_length=50, verbose_name="name of the club",
                            help_text="Input the name of club", null=False, blank=False)
    date_birth_club = models.DateField()

    def __str__(self):
        return "Club: " + self.name


class Footballer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="id CLUB",
                                help_text="Choose club", null=False, blank=False)
    Position = models.ForeignKey('Footballer.Position', on_delete=models.CASCADE)

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="Выберите id пользователя", null=True, blank=True)

    class Meta:
        app_label = "Footballer"

    def __str__(self):
        return "Footballer Name: " + self.first_name + " Last name: " + self.last_name


class Referee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    number_games = models.IntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="Выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Referee: " + self.first_name


class Division(models.Model):
    name_division = models.CharField(max_length=100, verbose_name="Name", help_text="Input the name", null=False,
                                     blank=False, primary_key=True)
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE, verbose_name="Referee",
                                help_text="Choose the referee", null=False, blank=False)#
    clubs = models.ManyToManyField(Club)


class Game(models.Model):
    number = models.IntegerField()
    footballer = models.ForeignKey(Footballer, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, verbose_name="Division",
                                 help_text="Input division", null=False, blank=False, default="RPL")
    goals = models.IntegerField()

    def __str__(self):
        return "Game with: " + self.footballer.first_name + " and referee: " + self.division.referee.last_name

