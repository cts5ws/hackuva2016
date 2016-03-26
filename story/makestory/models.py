from __future__ import unicode_literals

from django.db import models
from django.core.files import File
import os, urllib

# Create your models here.
class Image(models.Model):
    image_file = models.FileField(upload_to='images/')
    image_url = models.URLField()
    
def get_remote_image(self):
    if self.image_url and not self.image_file:
        result = urllib.urlretrieve(self.image_url)
        self.image_file.save(
            os.path.basename(self.image_url),
            File(open(result[0]))
        )
        self.save()