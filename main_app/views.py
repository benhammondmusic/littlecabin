import datetime
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# import custom User form
from .forms import UserForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

# for Google Calendar API
from .fetch_calendar import get_upcoming_events
from django.http import HttpResponse

# for DB models
from .models import Week, Postcard, Photo, User, Request
from django.views.generic.edit import CreateView #, UpdateView, DeleteView

# for AWS photos
import uuid
import boto3

# for config vars
from decouple import config

# load config vars (from .env locally, config vars on heroku)
S3_BASE_URL = config('S3_BASE_URL')
BUCKET = config('BUCKET')


#
# USER VIEWS / CLASSES
#
def home(request):
    return render(request, 'home.html')

def register(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('postcards')
        else:
            error_message = 'Invalid registration - try again'
            
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/register.html', context)

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


#
# CALENDAR VIEWS / CLASSES
#
@login_required
def calendar(request):
    if request.method == 'POST':
        display_year = request.POST['display_year']
    else: 
        display_year = datetime.date.today().year

    # ! NEED TO CHECK DB FIRST, THEN ONLY FETCH IF DB EVENTS ARE STALE/NOT SET YET
    events = get_upcoming_events(18*10, display_year)
    context = {"display_year": display_year, "events": events}
    return render(request, 'calendar.html', context)

class Create_Week(LoginRequiredMixin, CreateView):
    model = Week
    fields = '__all__'

#
# REQUEST VIEWS / CLASSES 
#
@login_required
def requests(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requests')
        else:
            error_message = 'Invalid Entry - try again'
            
    form = UserForm()
    unchecked_requests = Request.objects.filter(is_done = False).order_by('-created')
    checked_requests = Request.objects.filter(is_done = True).order_by('-created')
    context = {'form': form, 'error_message': error_message, 'unchecked_requests': unchecked_requests, 'checked_requests': checked_requests}
    return render(request, 'requests.html', context)

@login_required
def request_flip_is_done(request, request_id):
    request_to_flip = Request.objects.get(id=request_id)
    check_status = request_to_flip.is_done
    if check_status is True: 
        request_to_flip.is_done = False
    else:
        request_to_flip.is_done = True
    request_to_flip.save()
    return redirect('requests')

class Create_Request(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['item']
    def form_valid(self, form):
        form.instance.owner = self.request.user 
        return super().form_valid(form)      

@login_required
def requests_detail(request, request_id):
    return redirect('requests')


#
# POSTCARD VIEWS / CLASSES
#

@login_required
def postcards(request):

    all_postcards = Postcard.objects.all().order_by('-created')
    postcards_with_authors = []

    for postcard in all_postcards:
        author = User.objects.get(username=postcard.owner)
        postcards_with_authors.append({"postcard": postcard, "author": author})

    context = {"postcards_with_authors": postcards_with_authors}
    return render(request, 'postcards.html', context)

@login_required
def postcards_detail(request, postcard_id):
    postcard = Postcard.objects.get(id=postcard_id)
    context = { 'postcard': postcard }
    return render(request, 'postcards/detail.html', context)

class Create_Postcard(LoginRequiredMixin, CreateView):
    model = Postcard
    fields = ['greeting', 'message']
    def form_valid(self, form):
        form.instance.owner = self.request.user 
        return super().form_valid(form)  

@login_required
def add_photo(request, postcard_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, postcard_id=postcard_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('postcards')


#
# INFO VIEWS / CLASSES
#

@login_required
def info(request):
    return render(request, 'info.html')
