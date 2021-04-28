from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# VIEWS
def home(request):
    return render(request, 'home.html')

def postcards(request):
    return render(request, 'postcards.html')

def calendar(request):
    return render(request, 'calendar.html')

def requests(request):
    return render(request, 'requests.html')

def info(request):
    return render(request, 'info.html')


def register(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('postcards')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render register.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/register.html', context)

# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
