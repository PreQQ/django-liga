import genericpath
from django.shortcuts import render

# Create your views here.
def views(request):
    return render(request, "home.html")
    
def matches(request):
    return render(request)

def table(request):
    return render(request)

def statistics(request):
    return render(request)

def club(request):
    return render(request)

def player(request):
    return render(request)