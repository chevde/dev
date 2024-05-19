from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Annonce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

class UploadImage(models.Model):
    annonce = models.ForeignKey(Annonce, related_name='images', on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='photos/')
