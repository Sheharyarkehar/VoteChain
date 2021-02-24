from django.db import models
## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally

class MyFile(models.Model):
    file = models.ImageField(blank=False, null=False)
    # description = models.CharField(max_length=255)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
