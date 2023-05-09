import genericpath
from django.shortcuts import render

# Create your views here.
def views(request):
    return render(request, "home.html")
    
def matches(request):
    return render(request, "matches.html")

def table(request):
    teams = [1,2,3]
    return render(request, "table.html", {"teams": teams})

def statistics(request):
    return render(request, "statistics.html")

def club(request):
    return render(request, "club.html")

def player(request):
    return render(request, "player.html")