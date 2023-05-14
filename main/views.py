import genericpath
from django.shortcuts import get_object_or_404, render

from .models import Match

# Create your views here.
def views(request):
    return render(request, "home.html")
    
def matches(request):
    rows = [1,2,3,4,5]
    matches = [1,2,3,4,5]
    return render(request, "matches.html", {"matches": matches, "rows": rows})

def match(request, match_id):
    # matchFinder = get_object_or_404(Match, pk=match_id)
    return render(request, "match.html", {"match": match_id})

def table(request):
    teams = [1,2,3]
    return render(request, "table.html", {"teams": teams})

def statistics(request):
    return render(request, "statistics.html")

def club(request, club_id):
    players = [1,2,3,4]
    rows = [1,2,3,4,5]
    matches = [1,2,3,4,5]
    return render(request, "club.html", {"players": players, "matches": matches, "rows": rows})

def player(request, player_id):
    return render(request, "player.html", {"player": player_id})