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

    with open('mahmoud/q1.csv') as f:
        questions1 = list(csv.DictReader(f))
    with open('mahmoud/q3.csv') as f:
        questions3 = list(csv.DictReader(f))


class Subsession(BaseSubsession):
    def creating_session(self):
        print(Constants.questions1)
        for p in self.get_players():
            for q in Constants.questions1:
                Q1.objects.create(player=p, case_n=q['case'], cost=q['cost'],
                                  rule=bool(q['rule']),
                                  real_cost=float(q['realcost']),)

            for q in Constants.questions3:
                Q3.objects.create(player=p, option_a=q['option_a'], option_b=q['option_b'], type=q['type'], A=q['A'],
                                  B_false=q['B_false'], B_true=q['B_true'])

            num_q1 = Q1.objects.filter(player=p).count()
            num_q3a = Q3.objects.filter(player=p, type='a').count()
            num_q3b = Q3.objects.filter(player=p, type='b').count()
            num_q3c = Q3.objects.filter(player=p, type='c').count()
            p.selecting_q1 = int(Q1.objects.filter(player=p)[random.randint(0, num_q1 - 1)].case_n)
            p.selecting_q3a = random.randint(1, num_q3a)
            p.selecting_q3b = random.randint(1, num_q3b)
            p.selecting_q3c = random.randint(1, num_q3c)
            fields_to_do = ['dice_q1_d1',
                            'dice_q1_d2',
                            'dice_q2',
                            'dice_q3a',
                            'dice_q3b',
                            'dice_q3c', ]
            for f in fields_to_do:
                setattr(p, f, random.choice([True, False]))


class Group(BaseGroup):
    ...


class Player(BasePlayer):
    selecting_q1 = models.IntegerField()
    selecting_q3a = models.IntegerField()
    selecting_q3b = models.IntegerField()
    selecting_q3c = models.IntegerField()
    dice_q1_d1 = models.BooleanField()
    dice_q1_d2 = models.BooleanField()
    dice_q2 = models.BooleanField()
    dice_q3a = models.BooleanField()
    dice_q3b = models.BooleanField()
    dice_q3c = models.BooleanField()
    profit_q1 = models.FloatField()
    profit_q2 = models.FloatField()
    profit_q3a = models.FloatField()
    profit_q3b = models.FloatField()
    profit_q3c = models.FloatField()
    question2a = models.IntegerField(verbose_name='Keep (in CHF):')
    question2b = models.IntegerField(verbose_name='Play (in CHF):')
    gender = models.CharField(choices=['Male', 'Female'], widget=widgets.RadioSelectHorizontal)
    field_of_study = models.CharField(verbose_name='Field of study',
                                      choices=['Economics/finance', 'Other '], widget=widgets.RadioSelectHorizontal)
    level_of_study = models.CharField(choices=['Bachelor student', 'Master student'],
                                      widget=widgets.RadioSelectHorizontal)
    email=djmodels.EmailField(verbose_name='Enter emai')

    def set_payoffs(self):
        selected_decision_q1 = Q1.objects.get(player=self, case_n=self.selecting_q1)
        rule_q1 = selected_decision_q1.rule
        realcost_q = selected_decision_q1.real_cost
        q1_d1_win = selected_decision_q1.d1 * self.dice_q1_d1
        q1_d2_win = selected_decision_q1.d2 * self.dice_q1_d2
        if rule_q1:
            final_cost_q1 = realcost_q
        else:
            final_cost_q1 = selected_decision_q1.d1 * realcost_q
        self.profit_q1 = float(q1_d1_win) + float(q1_d2_win) - float(final_cost_q1)

        selected_decision_q3a = Q3.objects.filter(player=self, type='a')[self.selecting_q3a - 1]
        selected_decision_q3b = Q3.objects.filter(player=self, type='b')[self.selecting_q3b - 1]
        selected_decision_q3c = Q3.objects.filter(player=self, type='c')[self.selecting_q3c - 1]
        if selected_decision_q3a.answer:
            self.profit_q3a = selected_decision_q3a.A
        else:
            if self.dice_q3a:
                self.profit_q3a = selected_decision_q3a.B_true
            else:
                self.profit_q3a = selected_decision_q3a.B_false

        self.profit_q2 = self.question2a + self.question2b * 2 * self.dice_q2
        if selected_decision_q3b.answer:
            self.profit_q3b = selected_decision_q3b.A
        else:
            if self.dice_q3b:
                self.profit_q3b = selected_decision_q3b.B_true
            else:
                self.profit_q3b = selected_decision_q3b.B_false

        if selected_decision_q3c.answer:
            self.profit_q3c = selected_decision_q3c.A
        else:
            if self.dice_q3c:
                self.profit_q3c = selected_decision_q3c.B_true
            else:
                self.profit_q3c = selected_decision_q3c.B_false
        self.payoff = self.profit_q1 + self.profit_q2 + self.profit_q3a + self.profit_q3b + self.profit_q3c
        self.save()


class GeneralQuestion(djmodels.Model):
    player = models.ForeignKey(Player, related_name="%(app_label)s_%(class)s_question")

    class Meta:
        abstract = True
from django.core.validators import MaxValueValidator, MinValueValidator

class Q1(GeneralQuestion):
    case_n = models.CharField()
    cost = models.CharField()
    d1 = djmodels.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(Constants.q1endowment)],null=True)
    d2 = djmodels.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(Constants.q1endowment)],null=True)
    rule = models.BooleanField()
    real_cost= models.FloatField()


class Q3(GeneralQuestion):
    option_a = models.CharField()
    option_b = models.CharField()
    answer = models.BooleanField()
    type = models.CharField()
    A = models.FloatField()
    B_false = models.FloatField()
    B_true = models.FloatField()
