from django.db import models
class MyFile(models.Model):
    file = models.ImageField(blank=False, null=False)
    url = models.CharField(max_length=255)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
