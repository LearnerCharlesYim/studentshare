from django.db import models

# Create your models here.
class Banner(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    path = models.CharField(max_length=254)
    priority = models.IntegerField()

