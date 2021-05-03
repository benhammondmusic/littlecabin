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
from .models import Week, Postcard, Photo, User
from django.views.generic.edit import CreateView #, UpdateView, DeleteView

# for AWS photos
import uuid
import boto3

# for config vars
from decouple import config

# load config vars (from .env locally, config vars on heroku)
S3_BASE_URL = config('S3_BASE_URL')
BUCKET = config('BUCKET')


# VIEWS
def home(request):
    return render(request, 'home.html')

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
def calendar(request):
    # POST request comes with a display year; comes from user clicking "next year" btn/form on calendar
    if request.method == 'POST':
        display_year = request.POST['display_year']
    # GET request should display current year; comes from nav links, etc    
    else: 
        display_year = datetime.date.today().year

# ! NEED TO CHECK DB FIRST, THEN ONLY FETCH IF DB EVENTS ARE STALE/NOT SET YET
    events = get_upcoming_events(18*10, display_year)
    context = {"display_year": display_year, "events": events}
    return render(request, 'calendar.html', context)


@login_required
def requests(request):
    return render(request, 'requests.html')

@login_required
def info(request):
    return render(request, 'info.html')

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




class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class Create_Week(LoginRequiredMixin, CreateView):
    model = Week
    fields = '__all__'






# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
