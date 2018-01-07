from django.core.management import BaseCommand
from otree.models import Session
from testing_utils.models import AddedSession, ParticipantEmailLookup
from django.core.exceptions import ObjectDoesNotExist
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('session_code', nargs='+', type=str)


    # A command must define handle()
    def handle(self, *args, **options):
        sessions= options['session_code']
        for i in sessions:
            a= None
            try:
                a = Session.objects.get(code=i)
            except ObjectDoesNotExist:
                print('sorry no session like this: {}'.format(i))
                continue
            if a:
                ...
                new_rec, created = AddedSession.objects.get_or_create(session=a)

                for p in a.get_participants():
                    ParticipantEmailLookup.objects.get_or_create(participant=p)
        all_added_sessions = AddedSession.objects.all()
        all_lookups = ParticipantEmailLookup.objects.all()
        for a in all_added_sessions:
            print(a)
        for p in all_lookups:
            print(p.participant._url_i_should_be_on(),' ---', p.email)

        # self.stdout.write("Doing All The Things!")