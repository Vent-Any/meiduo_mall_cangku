from django.db import models

# Create your models here.
class UserScore(models.Model):
    total = models.PositiveIntegerField(default=0)