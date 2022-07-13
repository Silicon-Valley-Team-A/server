from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.FileField(upload_to = "uploaded_files/")
    uploadDate = models.DateTimeField(auto_now = True)