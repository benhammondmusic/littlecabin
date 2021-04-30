from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.urls import reverse


HEIRS = (
    ("0","TBD"), 
    ("1","Hammy"), 
    ("2","Toby"), 
    ("3","Connie"), 
    ("4","Cherie"), 
    ("5","Tom"), 
    ("6","Chris")
    )


# Class User already defined by Django


class Week(models.Model):
    owner = models.CharField(max_length=1, choices=HEIRS, default=HEIRS[0][0])
    users = models.ManyToManyField(User)
    start_date = models.DateField('Start Date')

    def __str__(self):
        return f'{self.start_date}-{self.get_owner_display()}'

    # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'week_id': self.id})


class Postcard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    greeting = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    photo_url = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


