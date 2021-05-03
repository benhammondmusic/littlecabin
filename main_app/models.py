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

    def get_absolute_url(self):
        return reverse('detail', kwargs={'week_id': self.id})


class Postcard(models.Model):
    # Postcard picture 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    greeting = models.CharField(max_length=50)
    message = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatedDate = self.created.strftime("%Y-%m-%d")
        return f'{self.greeting} - {self.owner} {formatedDate}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'postcard_id': self.id})  
        # class Meta:
        #     ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for postcard_id: {self.postcard_id} @{self.url}'


class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=300)
    isDone = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'request_id': self.id})  


class Agree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)    
