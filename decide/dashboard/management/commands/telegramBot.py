import random
import itertools


from django.core.management.base import BaseCommand
from telegramBot.echobot import main






class Command(BaseCommand):
    help = 'Test the full voting process with one auth (self)'



    def handle(self, *args, **options):
       main()