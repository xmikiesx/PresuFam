from django.db import models

# Create your models here.

class MyUser(models.Model):
    email = models.EmailField(max_length=200, help_text="Enter your name")


