from django.shortcuts import render

# VIEWS
def home(request):
    return render(request, 'home.html')

def calendar(request):
    return render(request, 'calendar.html')


# ! DELETE THIS
def koka(request):
    return render(request, 'koka.html')
