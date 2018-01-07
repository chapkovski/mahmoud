from otree.api import Currency as c, currency_range, Submission
from . import views, models
from ._builtin import Bot
from .models import Constants
import random

# Intro,
# Background,
# Question1,
# Question2,
# Question3a,
# Question3b,
# Question3c,
# Results,
['gender','field_of_study','level_of_study']

class PlayerBot(Bot):
    def play_round(self):

        yield (views.Intro)
        yield (views.Background,{
            'gender':random.choice(models.Player._meta.get_field('gender').choices),
            'field_of_study':random.choice(models.Player._meta.get_field('field_of_study').choices),
            'level_of_study':random.choice(models.Player._meta.get_field('level_of_study').choices),
        })


        # amount_sent = random.randint(0, self.participant.vars['herd_size'])
        # recipient = [p.id for p in self.player.sender.all()][0]
        fulfill_dict = {
            'q1_question-INITIAL_FORMS': (13,13),
            'q1_question-TOTAL_FORMS': (13,13),
            'INITIAL_FORMS': 13,
            'TOTAL_FORMS': 13,
            'q1_question-0-d1': 50,
            'q1_question-0-d2': 50,
            'q1_question-1-d1': 50,
            'q1_question-1-d2': 50,
            'q1_question-2-d1': 50,
            'q1_question-2-d2': 50,
            'q1_question-3-d1': 50,
            'q1_question-3-d2': 50,
            'q1_question-4-d1': 50,
            'q1_question-4-d2': 50,
            'q1_question-5-d1': 50,
            'q1_question-5-d2': 50,
            'q1_question-6-d1': 50,
            'q1_question-6-d2': 50,
            'q1_question-7-d1': 50,
            'q1_question-7-d2': 50,
            'q1_question-8-d1': 50,
            'q1_question-8-d2': 50,
            'q1_question-9-d1': 50,
            'q1_question-9-d2': 50,
            'q1_question-10-d1': 50,
            'q1_question-10-d2': 50,
            'q1_question-11-d1': 50,
            'q1_question-11-d2': 50,
            'q1_question-12-d1': 50,
            'q1_question-12-d2': 50,
            'q1_question-13-d1': 50,
            'q1_question-13-d2': 50,

        }
        # fulfill_dict=dict()
        yield Submission(views.Question1, fulfill_dict, check_html=False)
        yield (views.Results)

