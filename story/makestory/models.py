from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.

class Bigram(models.Model):
    first_word = models.CharField(max_length=25)
    next_word = models.CharField(max_length=25)
    frequency = models.IntegerField()
    
