from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Q3
import django
from django import forms
from .forms import Q1FormSet, Q3FormSet
from django.db.models import Q

class Intro(Page):
    ...
class Background(Page):
    form_model = models.Player
    form_fields = ['gender','field_of_study','level_of_study']
class Results(Page):
    ...
class QPage(Page):
    qn = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qn'] = self.qn
        return context


class Question1(QPage):
    qn = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = Q1FormSet(instance=self.player)
        return context

    def post(self):
        context = super().get_context_data()
        formset = Q1FormSet(self.request.POST, instance=self.player)
        context['formset'] = formset
        if not formset.is_valid():
            return self.render_to_response(context)
        formset.save()
        return super().post()


class Question2(QPage):
    qn = 2
    form_model = Player
    form_fields = ['question2a', 'question2b']

    def error_message(self, values):
        if values["question2a"] + values["question2b"] != Constants.q2endowment:
            return 'The numbers must add up to {}'.format(Constants.q2endowment)


class Question3(QPage):
    qtype = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Q3.objects.filter(player=self.player, type=self.qtype)
        print("QQQQ",queryset)
        context['formset'] = Q3FormSet(instance=self.player, queryset=queryset)
        return context

    def post(self):
        context = super().get_context_data()
        queryset = Q3.objects.filter(player=self.player, type=self.qtype)
        formset = Q3FormSet(self.request.POST, instance=self.player, queryset=queryset)
        context['formset'] = formset
        if not formset.is_valid():
            return self.render_to_response(context)
        formset.save()
        return super().post()


class Question3a(Question3):
    qn = '3a'
    qtype = 'a'
    template_name = 'mahmoud/Question3.html'


class Question3b(Question3):
    qn = '3b'
    qtype = 'b'
    template_name = 'mahmoud/Question3.html'

class Question3c(Question3):
    qn = '3c'
    qtype = 'c'
    template_name = 'mahmoud/Question3.html'

page_sequence = [
    Intro,
    Background,
    Question1,
    Question2,
    Question3a,
    Question3b,
    Question3c,
    Results,
]
