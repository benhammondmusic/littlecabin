import datetime
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# import custom User form
from .forms import UserForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

# for Google Calendar API
from .fetch_calendar import get_upcoming_events
from django.http import HttpResponse




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
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")

    display_year = datetime.date.today().year
    print("display year", display_year)


    events = get_upcoming_events(18*10, display_year)
    context = {"display_year": display_year, "events": events}
    return render(request, 'calendar.html', context)

# @login_required
# def show_year(request, display_year):

#     print("CAL_YR: display year", display_year)

#     events = get_upcoming_events(18*10, display_year)
#     context = {"display_year": display_year, "events": events}
#     return render(request, 'calendar.html', context)    

""" 
def assoc_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

 """


# def post_comment(request, new_comment):
#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#     c = comments.Comment(comment=new_comment)
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')


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
