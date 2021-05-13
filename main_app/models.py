from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.urls import reverse
from datetime import datetime


class Week(models.Model):
    owner_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # users = models.ManyToManyField(User)
    start_date = models.DateField('Start Date')

    def __str__(self):
        print("INSIDE WEEK MODEL", self.start_date)
        return f"[{self.start_date} - {str(self.owner_group)[2:]}]"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'week_id': self.id})


class Swap(models.Model):
    has_been_accepted = models.BooleanField(default=False)
    initiator= models.ForeignKey(User, on_delete=models.CASCADE)
    desired_week = models.ForeignKey(Week, related_name="desired_week", on_delete=models.CASCADE)
    offered_week = models.ForeignKey(Week, related_name="offered_week",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        print("INSDIE SWAP MODEL", self.desired_week)
        return f'{self.initiator.first_name} {self.initiator.last_name[0]}. wants {self.desired_week}; offers {self.offered_week}'

    def get_initiator_ownergroup(self):
        return self.initiator.groups.all().exclude(name="member").exclude(name="admin").first()

    def get_initiators_weeks(self):
        return Week.objects.filter(owner_group=self.get_initiator_ownergroup())

    def get_desired_week_ownergroup(self):
        group = Group.objects.get(name=self.desired_week.owner_group)
        return group
    
    def get_reciprocators(self):
        return User.objects.filter(groups__name=self.desired_week.owner_group)

    



class Postcard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    greeting = models.CharField(max_length=50)
    message = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatedDate = self.created.strftime("%m %d, %Y")
        
        return f'{self.greeting} - {self.owner} {formatedDate}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'postcard_id': self.id})  
        # class Meta:
        #     ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    alt_text = models.TextField(max_length=2000)
    postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for postcard_id: {self.postcard_id} @{self.url}'


class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=300)
    is_done = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'request_id': self.id})  


class Agree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)    
