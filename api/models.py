from django.db import models

# Create your models here.
class Item(models.Model):
    #name = models.CharField(max_length=100)
    #description = models.TextField(max_length=300)
    #cost = models.IntegerField()
    #address = models.TextField(max_length=500)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300, default="")
    price = models.IntegerField()
    video = models.FileField(upload_to='videos/', default="")
    verified = models.BooleanField(default=False)