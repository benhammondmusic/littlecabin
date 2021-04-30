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
from .models import Week, Postcard
from django.views.generic.edit import CreateView #, UpdateView, DeleteView



# VIEWS
def home(request):
    return render(request, 'home.html')

@login_required
def postcards(request):
    return render(request, 'postcards.html')

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

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class Create_Week(LoginRequiredMixin, CreateView):
    model = Week
    fields = '__all__'

class Create_Postcard(LoginRequiredMixin, CreateView):
    model = Postcard
    fields = '__all__'







# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
