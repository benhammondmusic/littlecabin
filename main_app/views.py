from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# import custom User form
from .forms import UserForm

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
    return render(request, 'calendar.html')

@login_required
def requests(request):
    return render(request, 'requests.html')

@login_required
def info(request):
    return render(request, 'info.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('postcards')
    else:
        form = UserForm()


    return render(request, 'registration/register.html', {'form': form})

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

# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
