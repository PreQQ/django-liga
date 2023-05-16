import genericpath
from django.shortcuts import get_object_or_404, render

from .models import Match, Team, Player, Event
from django.db.models import Count, Q
    
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
    tteams = list(Team.objects.values_list('name', "id"))
    events = list(Event.objects.values_list("event_type", "player"))
    print(tteams)
    print(events)
    TT = [];

    matches = list(Match.objects.all())

    def calcData(matches, TT):
        for match in matches:

            eventsTT = list(Event.objects.values_list("event_type", "match").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(pk=match.id))
            print(eventsTT)

    # match for 2 teams, only goals, add to 2 teams calc data (pts, w/d/l)


    calcData(matches, TT)

    teams = [1,2,3]
    return render(request, "table.html", {"teams": teams})

def statistics(request):
    players = list(Player.objects.all())

    goalsEvents = list(Event.objects.values_list("event_type", "player").filter(event_type = 'GOAL').values('player').annotate(total=Count('player')).order_by('-total'))[:5]
    goals = []

    for x in goalsEvents:
        goals.append(dict(total = x["total"], player = players[x["player"] - 1], index = goalsEvents.index(x) + 1))

    assistsEvents = list(Event.objects.values_list("event_type", "player").filter(event_type = 'ASST').values('player').annotate(total=Count('player')).order_by('-total'))[:5]
    assists = []

    for x in assistsEvents:
        assists.append(dict(total = x["total"], player = players[x["player"] - 1], index = assistsEvents.index(x) + 1))

    yellowsEvents = list(Event.objects.values_list("event_type", "player").filter(event_type = 'YCAR').values('player').annotate(total=Count('player')).order_by('-total'))[:5]
    yellows = []

    for x in yellowsEvents:
        yellows.append(dict(total = x["total"], player = players[x["player"] - 1], index = yellowsEvents.index(x) + 1))

    redsEvents = list(Event.objects.values_list("event_type", "player").filter(event_type = 'RCAR').values('player').annotate(total=Count('player')).order_by('-total'))[:5]
    reds = []

    for x in redsEvents:
        reds.append(dict(total = x["total"], player = players[x["player"] - 1], index = redsEvents.index(x) + 1))
        
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