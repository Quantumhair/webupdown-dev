from django.core.management.base import BaseCommand
from webupdownapp.rssrecords.tasks import *

class Command(BaseCommand):
    help = "Runs the scheduled RSS check task"

    def handle(self, *args, **options):
        try:
            AllUpdate()
        except:
            self.stdout.write('Had a problem')

        self.stdout.write('Done Updating via Heroku Scheduler')