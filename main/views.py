import genericpath
from django.shortcuts import get_object_or_404, render

from .models import Match, Team, Player, Event, Change
from django.db.models import Count, Q
    
def matches(request):
    teamsLength = Team.objects.count()
    rowsMax = (teamsLength - 1) * 2

    matchesTT = Match.objects.all()
    matches = [dict(round = i + 1, row = []) for i in range(rowsMax)]
    players = list(Player.objects.all())

    for match in matchesTT:
        host = 0
        guest = 0
        outcome = 0

        eventsTT = list(Event.objects.values_list("event_type", "match", "player").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

        for event in eventsTT:
            teamId = players[event[2]].team.id

            if teamId == match.host.id:
                host += 1
            elif teamId == match.guest.id:   
                guest += 1 

            
        if host - guest < 0:
            outcome = -1
        elif host - guest > 0:
            outcome = 1 

        for x in matches:
            if int(x["round"]) == int(match.match_round):
                x["row"].append(dict(id = match.id, date = match.date, match_round = match.match_round, goalsHost = host, goalsGuest = guest, outcome = outcome, host = match.host, guest = match.guest))

    return render(request, "matches.html", {"matches": matches,"rowsMax": rowsMax})

def match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    players = list(Player.objects.all())
    goals = list(Event.objects.all().filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

    hostGoals = 0
    guestGoals = 0

    eventsTT = list(Event.objects.values_list("event_type", "match", "player").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

    for event in eventsTT:
        teamId = players[event[2]].team.id

        if teamId == match.host.id:
            hostGoals += 1
        elif teamId == match.guest.id:   
            guestGoals += 1 

    changes = list(Change.objects.all().filter(match=match.id))

    changesHost = []
    changesGuest = []

    for change in changes:
        if change.in_player.team.id == match.host.id:
            changesHost.append(change)
        elif change.in_player.team.id == match.guest.id:
            changesGuest.append(change)


    eventsHost = {
        "shots": 0,
        "fouls": 0,
        "yellows": 0,
        "reds": 0,
        "pens": 0,
        "offsides": 0,
        "corners": 0,
        "freekicks": 0
    }

    eventsGuest = {
        "shots": 0,
        "fouls": 0,
        "yellows": 0,
        "reds": 0,
        "pens": 0,
        "offsides": 0,
        "corners": 0,
        "freekicks": 0
    }

    events = list(Event.objects.all().filter(match=match.id))

    for event in events:
        if event.player.team.id == match.host.id:
                if event.event_type == 'SHOT':
                    eventsHost["shots"] += 1
                elif event.event_type == 'FOUL':
                    eventsHost["fouls"] += 1
                elif event.event_type == 'YCAR':
                    eventsHost["yellows"] += 1
                elif event.event_type == 'RCAR':
                    eventsHost["reds"] += 1
                elif event.event_type == 'PENL':
                    eventsHost["pens"] += 1
                elif event.event_type == 'OFFS':
                    eventsHost["offides"] += 1
                elif event.event_type == 'CRNR':
                    eventsHost["corners"] += 1
                elif event.event_type == 'FKCK':
                    eventsHost["freekicks"] += 1
        elif event.player.team.id == match.guest.id:
                if event.event_type == 'SHOT':
                    eventsGuest["shots"] += 1
                elif event.event_type == 'FOUL':
                    eventsGuest["fouls"] += 1
                elif event.event_type == 'YCAR':
                    eventsGuest["yellows"] += 1
                elif event.event_type == 'RCAR':
                    eventsGuest["reds"] += 1
                elif event.event_type == 'PENL':
                    eventsGuest["pens"] += 1
                elif event.event_type == 'OFFS':
                    eventsGuest["offides"] += 1
                elif event.event_type == 'CRNR':
                    eventsGuest["corners"] += 1
                elif event.event_type == 'FKCK':
                    eventsGuest["freekicks"] += 1

    return render(request, "match.html", {"match": match, "goals": goals, "hostGoals": hostGoals, "guestGoals": guestGoals, "eventsHost": eventsHost, "eventsGuest": eventsGuest, "changesHost": changesHost, "changesGuest": changesGuest})

def table(request):
    players = list(Player.objects.all())
    TT = []

    matches = list(Match.objects.all())

    def calculateTable(matches, TT):
        for match in matches:
            host = 0
            guest = 0
            outcome = 0

            eventsTT = list(Event.objects.values_list("event_type", "match", "player").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

            for event in eventsTT:
                teamId = players[event[2]].team.id

                if teamId == match.host.id:
                    host += 1
                elif teamId == match.guest.id:   
                    guest += 1 

            
            if host - guest < 0:
                outcome = -1
            elif host - guest > 0:
                outcome = 1 

            foundHost = False

            for x in TT:
                if x["id"] == match.host.id:
                    foundHost = True
                    pts = 0
                    w = 0
                    d = 0
                    l = 0
                    if outcome == 1:
                        pts = 3
                        w = 1
                    elif outcome == 0:
                        pts = 1
                        d = 1
                    elif outcome == -1:
                        pts = 0
                        l = 1

                    x["mp"]+= 1
                    x["w"]+= w
                    x["d"]+= d
                    x["l"]+= l
                    x["gf"]+= host
                    x["ga"]+= guest
                    x["gd"]+= (host - guest)
                    x["pts"]+= pts
                    
                    if len(x["matches"]) > 5:
                        x["matches"].pop()
                        x["matches"].insert(0, pts)
                    else:
                        x["matches"].insert(0, pts)
                    break

            if foundHost == False:
                pts = 0
                w = 0
                d = 0
                l = 0
                if outcome == 1:
                    pts = 3
                    w = 1
                elif outcome == 0:
                    pts = 1
                    d = 1
                elif outcome == -1:
                    pts = 0
                    l = 1

                TT.append(dict(id = match.host.id, name = match.host.name, mp = 1, w = w, d = d, l = l, gf = host, ga = guest, gd = host - guest, pts = pts, matches = [pts], index = len(TT) + 1))

            foundGuest = False

            for x in TT:
                if x["id"] == match.guest.id:
                    foundGuest = True
                    pts = 0
                    w = 0
                    d = 0
                    l = 0
                    if outcome == -1:
                        pts = 3
                        w = 1
                    elif outcome == 0:
                        pts = 1
                        d = 1
                    elif outcome == 1:
                        pts = 0
                        l = 1

                    x["mp"]+= 1
                    x["w"]+= w
                    x["d"]+= d
                    x["l"]+= l
                    x["gf"]+= guest
                    x["ga"]+= host
                    x["gd"]+= (guest - host)
                    x["pts"]+= pts
                    
                    if len(x["matches"]) > 5:
                        x["matches"].pop()
                        x["matches"].insert(0, pts)
                    else:
                        x["matches"].insert(0, pts)
                    break

            if foundGuest == False:
                pts = 0
                w = 0
                d = 0
                l = 0
                if outcome == -1:
                    pts = 3
                    w = 1
                elif outcome == 0:
                    pts = 1
                    d = 1
                elif outcome == 1:
                    pts = 0
                    l = 1

                TT.append(dict(id = match.guest.id, name = match.guest.name, mp = 1, w = w, d = d, l = l, gf = guest, ga = host, gd = guest - host, pts = pts, matches = [pts], index = len(TT) + 1))


    calculateTable(matches, TT)
    return render(request, "table.html", {"teams": TT})

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
    teamsLength = Team.objects.count()
    rowsMax = (teamsLength - 1) * 2

    matchesTT = Match.objects.all().filter(Q(host=club_id) | Q(guest=club_id))
    matches = [dict(round = i + 1, row = []) for i in range(rowsMax)]
    players = list(Player.objects.all())

    for match in matchesTT:
        host = 0
        guest = 0
        outcome = 0

        eventsTT = list(Event.objects.values_list("event_type", "match", "player").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

        for event in eventsTT:
            teamId = players[event[2]].team.id

            if teamId == match.host.id:
                host += 1
            elif teamId == match.guest.id:   
                guest += 1 

            
        if host - guest < 0:
            outcome = -1
        elif host - guest > 0:
            outcome = 1 

        for x in matches:
            if int(x["round"]) == int(match.match_round):
                x["row"].append(dict(id = match.id, date = match.date, match_round = match.match_round, goalsHost = host, goalsGuest = guest, outcome = outcome, host = match.host, guest = match.guest))

    return render(request, "club.html", {"team": team, "players": players, "matches": matches, "rowsMax": rowsMax})

def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "player.html", {"player": player})

def players(request):
    playersArray = list(Player.objects.all())

    return render(request, "players.html", {"players": playersArray})