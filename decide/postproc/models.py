from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    MALE = 'M'
    WOMEN = 'W'
    OTHER = 'O'

    genre_choices = ((MALE, 'Hombre'), (WOMEN, 'Mujer'), (OTHER, 'Otro'))

    genre = models.CharField(max_length=1, choices=genre_choices, default=OTHER)
    user = models.OneToOneField(User, on_delete=models.CASCADE)