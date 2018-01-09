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
    form_fields = ['gender', 'field_of_study', 'level_of_study']


class Results(Page):
    form_model = models.Player
    form_fields = ['email']
    # def vars_for_template(self):
    #     self.player.set_payoffs()


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

    def before_next_page(self):
        self.player.dump_q1 = self.player.mahmoud_q1_question.all().values('case_n', 'd1', 'd2')


class Question2(QPage):
    qn = 2
    form_model = Player
    form_fields = ['question2a', 'question2b']

    def error_message(self, values):
        if values["question2a"] + values["question2b"] != Constants.q2endowment:
            return 'The numbers must add up to {}'.format(Constants.q2endowment)


class Question3(QPage):
    qtype = None
    template_name = 'mahmoud/Question3.html'
    @property
    def queryset(self):
        return self.player.mahmoud_q3_question.filter(type=self.qtype)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = Q3FormSet(instance=self.player, queryset=self.queryset)
        return context

    def post(self):
        context = super().get_context_data()
        formset = Q3FormSet(self.request.POST, instance=self.player, queryset=self.queryset)
        context['formset'] = formset
        if not formset.is_valid():
            return self.render_to_response(context)
        formset.save()
        return super().post()

    def before_next_page(self):
        q = self.queryset.values(
            'option_a',
            'option_b',
            'answer')
        for i in q:
            i['answer'] = i['option_a'] if i['answer'] else i['option_b']

        setattr(self.player, 'dump_q{}'.format(self.qn), q)
        self.player.save()


class Question3a(Question3):
    qn = '3a'
    qtype = 'a'



class Question3b(Question3):
    qn = '3b'
    qtype = 'b'



class Question3c(Question3):
    qn = '3c'
    qtype = 'c'


    def before_next_page(self):
        super().before_next_page()
        self.player.set_payoffs()


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
