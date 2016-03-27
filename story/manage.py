#!/usr/bin/env python
import os
import sys
#from models import Bigram

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "story.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

def create_db():
    BASE = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(BASE, 'makestory/output.txt'), 'r')
    instances = [
        Bigram(
            first_word = line.split()[0],
            next_word = line.split()[1],
            frequency = line.split()[2],
        )
        for line in f
    ]
    Bigram.objects.bulk_create(instances)
    f.close()