#!/usr/bin/env python
import os
import sys
from django.core.management.base import BaseCommand
# from models import Bigram

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "story.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

# class Command(BaseCommand):    
#     def create_db(self):
#         BASE = os.path.dirname(os.path.abspath("manage.py"))
#         f = open(os.path.join(BASE, 'makestory/output.txt'), 'r')
#         instances = [
#             Bigram(
#                 frequency = int(line.split()[0]),
#                 first_word = line.split()[1],
#                 next_word = line.split()[2],
#             )
#             for line in f
#         ]
#         Bigram.objects.bulk_create(instances)
#         f.close()