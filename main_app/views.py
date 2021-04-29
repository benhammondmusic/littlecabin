from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# import custom User form
from .forms import UserForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

# for Google Calendar API
from .fetch_calendar import get_next_10_events


# when start to use classes
# from django.contrib.auth.mixins import LoginRequiredMixin
# class EntityCreate(LoginRequiredMixin, CreateView): 

# VIEWS
def home(request):
    return render(request, 'home.html')

@login_required
def postcards(request):
    return render(request, 'postcards.html')

@login_required
def calendar(request):
    events= get_next_10_events()
    
    context = {"events": events}
    return render(request, 'calendar.html', context)

@login_required
def requests(request):
    return render(request, 'requests.html')

@login_required
def info(request):
    return render(request, 'info.html')

# def register(request):
#   error_message = ''
#   if request.method == 'POST':
#     # This is how to create a 'user' form object
#     # that includes the data from the browser
#     form = UserForm(request.POST)
#     if form.is_valid():
#       # This will add the user to the database
#       user = form.save()
#       # This is how we log a user in via code
#       login(request, user)
#       return redirect('postcards')
#     else:
#       print("!!")
#       error_message = 'Invalid sign up - try again'
#   # A bad POST or a GET request, so render register.html with an empty form
#   form = UserForm()
#   context = {'form': form, 'error_message': error_message}
#   return render(request, 'registration/register.html', context)
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('postcards')
    else:
        form = UserForm()

    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm






# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
