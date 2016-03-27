from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.

class Line(models.Model):
    frequencey = models.IntegerField()
    word1 = models.CharField()
    word2 = models.CharField()
    word3 = models.CharField()
    word4 = models.CharField()