from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django.db import models as djmodels

author = 'Your name here'

doc = """
Your app description
"""

from otree.models import Participant, Session


class AddedSession(djmodels.Model):
    session = djmodels.OneToOneField(to=Session)
    def __str__(self):
        return 'Added session {}'.format(self.session.code)


class ParticipantEmailLookup(djmodels.Model):
    email = djmodels.EmailField(blank=True, null=True)
    participant = djmodels.OneToOneField(to=Participant)
    def __str__(self):
        participant_url = self.participant._url_i_should_be_on()
        return 'PEL: {}, {}'.format(self.email, participant_url)
        # return 'somthing'
    def get_absolute_url(self):
        print('I AM IN ABSOLUTE URL AND GOING TO REDIRECT TO:', self.participant._url_i_should_be_on())
        return self.participant._url_i_should_be_on()

class Constants(BaseConstants):
    name_in_url = 'testing_utils'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    ...


class Group(BaseGroup):
    ...


class Player(BasePlayer):
    test = models.CharField(verbose_name='Please insert your Amazon mTurk ID')
