from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    mobile = models.CharField(max_length=64,null=True,blank=True)
    gender_choice = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(choices=gender_choice)
    birthdate = models.DateField()
# Create your models here.
