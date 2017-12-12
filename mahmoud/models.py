from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django.db import models as djmodels
from django.db.models import Q, Sum
import csv

author = 'Philip Chapkovski, UZH'

doc = """Risk game for Mahmoud Ola, University of St. Gallen"""


class Constants(BaseConstants):
    name_in_url = 'mahmoud'
    players_per_group = None
    num_rounds = 1
    q1endowment = 100
    q2endowment = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        with open('mahmoud/q1.csv') as f:
            questions1 = list(csv.DictReader(f))
        with open('mahmoud/q3.csv') as f:
            questions3 = list(csv.DictReader(f))
        for p in self.get_players():
            for q in questions1:
                Q1.objects.create(player=p, case_n=q['case'], cost=q['cost'])

            for q in questions3:
                Q3.objects.create(player=p, option_a=q['option_a'], option_b=q['option_b'], type=q['type'])


class Group(BaseGroup):
    ...


class Player(BasePlayer):
    question2a = models.IntegerField(verbose_name='Keep (in CHF):')
    question2b = models.IntegerField(verbose_name='Play (in CHF):')
    gender = models.CharField(choices=['Male', 'Female'], widget=widgets.RadioSelectHorizontal)
    field_of_study = models.CharField(verbose_name='Field of study',
                                      choices=['Economics/finance', 'Other '], widget=widgets.RadioSelectHorizontal)
    level_of_study= models.CharField(choices=['Bachelor student',    'Master student'], widget=widgets.RadioSelectHorizontal)


class GeneralQuestion(djmodels.Model):
    player = models.ForeignKey(Player, related_name="%(app_label)s_%(class)s_question")

    class Meta:
        abstract = True


class Q1(GeneralQuestion):
    case_n = models.CharField()
    cost = models.CharField()
    d1 = models.IntegerField()
    d2 = models.IntegerField()


class Q3(GeneralQuestion):
    option_a = models.CharField()
    option_b = models.CharField()
    answer = models.BooleanField()
    type = models.CharField()
