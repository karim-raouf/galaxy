from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
    

class TestApp(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500 , null=True)
    
    
    def __str__(self):
        return self.name
    



    