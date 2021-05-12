import datetime
import calendar as calendar_lib
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# import custom User form
from .forms import UserForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import user_passes_test

# for Google Calendar API
from .fetch_calendar import get_upcoming_events
from django.http import HttpResponse

from .populate_calendar import populate_google_calendar

# for DB models
from .models import Week, Postcard, Photo, User, Request, Swap
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# for AWS photos
import uuid
import boto3

# for config vars
from decouple import config

# load config vars (from .env locally, config vars on heroku)
S3_BASE_URL = config('S3_BASE_URL')
BUCKET = config('BUCKET')


# def oauth2callback(request):
#     print("callback fn from google cal api oath register")
#     print(request)
#     return redirect('calendar')

#
# USER VIEWS / CLASSES
#

def is_family_member(user):
    if not user.is_active:
       return False
    return user.groups.filter(name='member').exists()

def is_admin(user):
    if not user.is_active:
       return False
    return user.groups.filter(name='admin').exists()

def get_pending_users(user):
    pending_users = []
    if user.is_active and user.groups.filter(name='admin').exists():
        pending_users = User.objects.all().exclude(groups__name='member')
    return pending_users

# called from within a home/ post request
def approve_user(pending_user_id, pending_user_ownergroup):
    pending_user = User.objects.get(id=pending_user_id)
    
    # add user to generic "member" group
    member_group = Group.objects.get(name="member")
    member_group.user_set.add(pending_user)

    # also add user to their specific owner group
    owner_group = Group.objects.get(name=pending_user_ownergroup)
    owner_group.user_set.add(pending_user)
    return


def deny_user(request, pending_user_id):
    pending_user = User.objects.get(id=pending_user_id)
    pending_user.delete()
    return redirect('home')


def home(request):
    if request.method == 'POST':
        approve_user(request.POST["pending_user_id"], request.POST["pending_user_ownergroup"])
        return redirect('home')

    pending_users = get_pending_users(request.user)
    owner_groups = Group.objects.all().exclude(name="admin").order_by('name')
    context = {"pending_users": pending_users, "owner_groups":owner_groups}
    return render(request, 'home.html', context)

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
def pending(request):
    return render(request, 'registration/pending.html')    

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


#
# CALENDAR VIEWS / CLASSES
#
@user_passes_test(is_family_member, login_url='/accounts/pending')
def calendar(request):
    if request.method == 'POST':
        display_year = request.POST['display_year']
    else: 
        display_year = datetime.date.today().year

    events = Week.objects.filter(start_date__year=display_year).order_by('start_date')

    # if user has a pending swap, don't display the swap buttons
    current_user_has_pending_swaps = Swap.objects.filter(initiator=request.user).filter(has_been_accepted=False).exists()

    # format events and add user group info
    for event in events:
        formatted_start_date = event.start_date.strftime("%b %-d")
        event.start_date = formatted_start_date

        current_user_ownergroup = request.user.groups.all().exclude(name="member").exclude(name="admin").first()
        event.display_swap_btn = True
        if current_user_has_pending_swaps:
            event.display_swap_btn = False
        if event.owner_group == current_user_ownergroup:
            event.display_swap_btn = False
        if current_user_ownergroup == None:
            event.display_swap_btn = False
    
    # collect relevant swaps
    incoming_swaps = []
    outgoing_swaps = []
    swaps = Swap.objects.filter(has_been_accepted=False)
    for swap in swaps:
        if swap.get_initiator_ownergroup() == current_user_ownergroup:
            outgoing_swaps.append(swap)
        elif swap.get_desired_week_ownergroup() == current_user_ownergroup:
            incoming_swaps.append(swap)

    context = {"display_year": display_year, "events": events, "outgoing_swaps":outgoing_swaps, "incoming_swaps":incoming_swaps}
    return render(request, 'calendar.html', context)

class Create_Week(LoginRequiredMixin, CreateView):
    model = Week
    fields = '__all__'


# generate week events for testing
def reset_weeks(request):

    # delete all existing weeks from DB
    Week.objects.all().delete()


    ownergroups = Group.objects.all().exclude(name="member").exclude(name="admin").order_by('name')

    # build Weeks for the next 10 years 
    for yr in range(2021, 2023):
        month = calendar_lib.monthcalendar(yr, 5)
        may_mondays = [week[0] for week in month if week[0]>0]

        first_start_date = datetime.datetime(yr, 5, may_mondays[-1])
        weeks_later = datetime.timedelta(days=7)
        # each owner_group gets 3 weeks per year, in rotation
        for i in range(len(ownergroups) * 3):
            # weeks rotate through owner_groups 2 ways: 
            # YEARLY-the first week of the season will start with the next sibling in line from the previous year's first week
            # WEEKLY-every week of the 3-per owner season, the owner will advance from the previous week's owner
            week = Week(start_date=first_start_date + (i*weeks_later), owner_group=ownergroups[(yr-1+i) % len(ownergroups) ])
            week.save()

    all_weeks = Week.objects.all()

    # push to Google Calendar
    populate_google_calendar(all_weeks)


    return redirect('calendar')




#
# Swap
#
def propose_swap(request, week_id):
    initiator = request.user # User
    desired_week = Week.objects.get(id=week_id) # Week
    
    initiator_ownergroup = initiator.groups.all().exclude(name="member").exclude(name="admin").first()
    
    initiators_weeks = Week.objects.filter(owner_group=initiator_ownergroup)
    offered_week = initiators_weeks[0]

    swap = Swap(initiator=initiator,desired_week=desired_week, offered_week=offered_week)
    swap.save()

    return redirect('calendar')


def approve_swap(request, swap_id):
    swap = Swap.objects.get(id=swap_id)
    
    desired_week = swap.desired_week
    offered_week = swap.offered_week

    temp_owner_group = swap.get_desired_week_ownergroup()
    desired_week.owner_group =  offered_week.owner_group
    offered_week.owner_group = temp_owner_group
    swap.has_been_accepted = True
    swap.save()
    desired_week.save()
    offered_week.save()

    return redirect('calendar')

class Delete_Swap(LoginRequiredMixin, DeleteView):
    model = Swap
    fields = '__all__'
    success_url = '/calendar/'


#
# REQUEST VIEWS / CLASSES 
#
@user_passes_test(is_family_member, login_url='/accounts/pending')
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

    today = datetime.datetime.now()
    past_year_requests = Request.objects.filter(created__year=today.year)
    past_year_complete = Request.objects.filter(created__year=today.year).filter(is_done=True)
    completion_rate_past_year = 0
    if len(past_year_requests) > 0:
        completion_rate_past_year = int(100 * len(past_year_complete) / len(past_year_requests))

    user_requests = Request.objects.filter(owner=request.user)
    user_complete = Request.objects.filter(owner=request.user).filter(is_done=True)
    completion_rate_user = 0
    show_user_bar = False
    if len(user_requests) > 0:
        show_user_bar = True
        completion_rate_user = int(100 * len(user_complete) / len(user_requests))

    unchecked_requests = Request.objects.filter(is_done = False).filter(is_hidden = False).order_by('-created')
    checked_requests = Request.objects.filter(is_done = True).filter(is_hidden = False).order_by('-created')

    context = {'form': form, 'error_message': error_message, 'unchecked_requests': unchecked_requests, 'checked_requests': checked_requests, 'completion_rate_user': completion_rate_user, "completion_rate_past_year": completion_rate_past_year, "show_user_bar": show_user_bar}
    return render(request, 'requests.html', context)

@user_passes_test(is_family_member, login_url='/accounts/pending')
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

class Update_Request(LoginRequiredMixin, UpdateView):
    model = Request
    fields = ['item']  

@user_passes_test(is_family_member, login_url='/accounts/pending')
def requests_detail(request, request_id):
    return redirect('requests')

@user_passes_test(is_family_member, login_url='/accounts/pending')
def hide_completed_requests(request):
    checked_requests = Request.objects.filter(is_done = True)
    for todo in checked_requests:
        todo.is_hidden = True
        todo.save()

    return redirect('requests')


#
# POSTCARD VIEWS / CLASSES
#

@user_passes_test(is_family_member, login_url='/accounts/pending')
def postcards(request):

    all_postcards = Postcard.objects.all().order_by('-created')
    postcards_with_authors = []

    for postcard in all_postcards:
        author = User.objects.get(username=postcard.owner)
        postcards_with_authors.append({"postcard": postcard, "author": author})
    
    tilt_options = [-2,-1,0,1,2] 

    context = {"postcards_with_authors": postcards_with_authors, "tilt_options": tilt_options}
    return render(request, 'postcards.html', context)

@user_passes_test(is_family_member, login_url='/accounts/pending')
def postcards_detail(request, postcard_id):
    postcard = Postcard.objects.get(id=postcard_id)
    photos = Photo.objects.filter(postcard_id=postcard_id)
    
    context = { 'postcard': postcard, "photos": photos }
    return render(request, 'postcards/detail.html', context)

class Create_Postcard(LoginRequiredMixin, CreateView):
    model = Postcard
    fields = ['greeting', 'message']
    def form_valid(self, form):
        form.instance.owner = self.request.user 
        return super().form_valid(form)  

class Update_Postcard(LoginRequiredMixin, UpdateView):
  model = Postcard
  fields = ['greeting', 'message']

class Delete_Postcard(LoginRequiredMixin, DeleteView, ):
  model = Postcard
  success_url = '/postcards/'

  # overriding built in method
  def get_context_data(self, **kwargs):
        # set context object as normal
        context = super().get_context_data(**kwargs)
        # get id of postcard to be deleted
        postcard_id = context["object"].id
        # find the photo object whose postcard_id matches the postcard to be deleted
        # add it to the context to send along to our template
        context["photos"] = Photo.objects.filter(postcard_id=postcard_id)
        return context

@user_passes_test(is_family_member, login_url='/accounts/pending')
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

@user_passes_test(is_family_member, login_url='/accounts/pending')
def info(request):
    return render(request, 'info.html')
