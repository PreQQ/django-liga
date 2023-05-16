import genericpath
from django.shortcuts import get_object_or_404, render

from .models import Match, Team, Player, Event
from django.db.models import Count 
    
def matches(request):
    teamsLength = Team.objects.count()
    rowsMax = (teamsLength - 1) * 2

    matchess = Match.objects.all()
    print(matchess)
    rows = [1,2,3,4,5]
    matches = [1,2,3,4,5]
    return render(request, "matches.html", {"matches": matches, "rows": rows, "rowsMax": rowsMax})

def match(request, match_id):
    # matchFinder = get_object_or_404(Match, pk=match_id)
    return render(request, "match.html", {"match": match_id})

def table(request):
    tteams = list(Team.objects.all().values_list('name', flat=True)) 
    print(tteams)
    teams = [1,2,3]
    return render(request, "table.html", {"teams": teams})

def statistics(request):
    # goalss = list(Event.objects.values_list("event_type", "player").filter(event_type = 'GOAL').values('player').annotate(total=Count('player')).order_by('-total'))
    goalss = Player.objects.annotate(List=Count('event'), total=Count('event__event_type'))
    print(goalss)
    goals = [1,2,3,4,5]
    assists = [1,2,3,4,5]
    yellows = [1,2,3,4,5]
    reds = [1,2,3,4]
    return render(request, "statistics.html", {"goals": goals, "assists": assists, "yellows": yellows, "reds": reds})

def club(request, club_id):
    team = get_object_or_404(Team, pk=club_id)
    players = list(team.player_set.all())
    rows = [1,2,3,4,5]
    matches = [1,2,3,4,5]
    return render(request, "club.html", {"team": team, "players": players, "matches": matches, "rows": rows})

def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "player.html", {"player": player})