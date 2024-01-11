from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    username= models.CharField(max_length=225,unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]