import genericpath
from django.shortcuts import get_object_or_404, render, redirect

from .models import Match, Team, Player, Event, Change
from django.db.models import Count, Q

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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
            teamId = [player for player in players if player.id == event[2]][0].team.id

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
        teamId = [player for player in players if player.id == event[2]][0].team.id

        if teamId == match.host.id:
            hostGoals += 1
        elif teamId == match.guest.id:   
            guestGoals += 1 

    pitchTeamHost = [None, None, None, None, None, None, None, None, None, None, None]
    pitchTeamGuest = [None, None, None, None, None, None, None, None, None, None, None]

    playersHost = list(Player.objects.all().filter(team=match.host.id))
    playersGuest = list(Player.objects.all().filter(team=match.guest.id))

    for i in playersHost:
        player = i.position
        if player == 'GK' and pitchTeamHost[0] == None:
            pitchTeamHost[0] = i
        elif player == 'LB' and pitchTeamHost[1] == None:
            pitchTeamHost[1] = i
        elif player == 'CB' and (pitchTeamHost[2] == None or pitchTeamHost[3] == None):
            if pitchTeamHost[2] != None:
                pitchTeamHost[3] = i
            else:
                pitchTeamHost[2] = i
        elif player == 'RB' and pitchTeamHost[4] == None:
            pitchTeamHost[4] = i
        elif player == 'LM' and pitchTeamHost[5] == None:
            pitchTeamHost[5] = i
        elif player == 'RM' and pitchTeamHost[6] == None:
            pitchTeamHost[6] = i
        elif player == 'CM' and pitchTeamHost[7] == None:
            pitchTeamHost[7] = i
        elif player == 'LS' and pitchTeamHost[8] == None:
            pitchTeamHost[8] = i
        elif player == 'RS' and pitchTeamHost[9] == None:
            pitchTeamHost[9] = i
        elif player == 'CS' and pitchTeamHost[10] == None:
            pitchTeamHost[10] = i

    for i in playersGuest:
        player = i.position
        if player == 'GK' and pitchTeamGuest[0] == None:
            pitchTeamGuest[0] = i
        elif player == 'LB' and pitchTeamGuest[1] == None:
            pitchTeamGuest[1] = i
        elif player == 'CB' and (pitchTeamGuest[2] == None or pitchTeamGuest[3] == None):
            if pitchTeamGuest[2] != None:
                pitchTeamGuest[3] = i
            else:
                pitchTeamGuest[2] = i
        elif player == 'RB' and pitchTeamGuest[4] == None:
            pitchTeamGuest[4] = i
        elif player == 'LM' and pitchTeamGuest[5] == None:
            pitchTeamGuest[5] = i
        elif player == 'RM' and pitchTeamGuest[6] == None:
            pitchTeamGuest[6] = i
        elif player == 'CM' and pitchTeamGuest[7] == None:
            pitchTeamGuest[7] = i
        elif player == 'LS' and pitchTeamGuest[8] == None:
            pitchTeamGuest[8] = i
        elif player == 'RS' and pitchTeamGuest[9] == None:
            pitchTeamGuest[9] = i
        elif player == 'CS' and pitchTeamGuest[10] == None:
            pitchTeamGuest[10] = i

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

    return render(request, "match.html", {"match": match, "goals": goals, "hostGoals": hostGoals, "guestGoals": guestGoals, "eventsHost": eventsHost, "eventsGuest": eventsGuest, "changesHost": changesHost, "changesGuest": changesGuest, "pitchTeamHost": pitchTeamHost, "pitchTeamGuest": pitchTeamGuest})

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
                teamId = [player for player in players if player.id == event[2]][0].team.id

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

                TT.append(dict(id = match.host.id, name = match.host.name, mp = 1, w = w, d = d, l = l, gf = host, ga = guest, gd = host - guest, pts = pts, matches = [pts]))

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

                TT.append(dict(id = match.guest.id, name = match.guest.name, mp = 1, w = w, d = d, l = l, gf = guest, ga = host, gd = guest - host, pts = pts, matches = [pts]))


    calculateTable(matches, TT)
    newlist = sorted(TT, key=lambda d: d['pts'], reverse=True)

    indexList = []

    for i in range(len(newlist)):
        indexList.append(i + 1)
    
    return render(request, "table.html", {"teams": newlist, "indexes": indexList})

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


    #max/min/srednia goli w meczu w sezonie
    goalsData = list(Event.objects.values_list("event_type", "match").filter(event_type = 'GOAL').values('match').annotate(total=Count('match')).order_by('-total'))

    goalsMax = max(goalsData, key=lambda x:x['total'])
    goalsMin = min(goalsData, key=lambda x:x['total'])
    goalsAvg = 0 if len(goalsData) == 0 else sum(item['total'] for item in goalsData)/len(goalsData)

    goalsExtra = {
        "max": goalsMax["total"],
        "min": goalsMin["total"],
        "avg": goalsAvg
    }

    #max/min/srednia asyst w meczu w sezonie
    assistsData = list(Event.objects.values_list("event_type", "match").filter(event_type = 'ASST').values('match').annotate(total=Count('match')).order_by('-total'))
    
    assistsMax = max(assistsData, key=lambda x:x['total'])
    assistsMin = min(assistsData, key=lambda x:x['total'])
    assistsAvg = 0 if len(assistsData) == 0 else sum(item['total'] for item in assistsData)/len(assistsData)

    assistsExtra = {
        "max": assistsMax["total"],
        "min": assistsMin["total"],
        "avg": assistsAvg
    }

    #max/min/srednia zoltych kartek w meczu w sezonie
    yellowsData = list(Event.objects.values_list("event_type", "match").filter(event_type = 'YCAR').values('match').annotate(total=Count('match')).order_by('-total'))
    
    yellowsMax = max(yellowsData, key=lambda x:x['total'])
    yellowsMin = min(yellowsData, key=lambda x:x['total'])
    yellowsAvg = 0 if len(yellowsData) == 0 else sum(item['total'] for item in yellowsData)/len(yellowsData)

    yellowsExtra = {
        "max": yellowsMax["total"],
        "min": yellowsMin["total"],
        "avg": yellowsAvg
    }

    #max/min/srednia czerwonych kartek w meczu w sezonie
    redsData = list(Event.objects.values_list("event_type", "match").filter(event_type = 'RCAR').values('match').annotate(total=Count('match')).order_by('-total'))
    
    redsMax = max(redsData, key=lambda x:x['total'])
    redsMin = min(redsData, key=lambda x:x['total'])
    redsAvg = 0 if len(redsData) == 0 else sum(item['total'] for item in redsData)/len(redsData)

    redsExtra = {
        "max": redsMax["total"],
        "min": redsMin["total"],
        "avg": redsAvg
    }
        
    return render(request, "statistics.html", {"goals": goals, "assists": assists, "yellows": yellows, "reds": reds, "goalsExtra": goalsExtra, "assistsExtra": assistsExtra, "yellowsExtra": yellowsExtra, "redsExtra": redsExtra})

def club(request, club_id):
    team = get_object_or_404(Team, pk=club_id)
    teamsLength = Team.objects.count()
    rowsMax = (teamsLength - 1) * 2

    matchesTT = Match.objects.all().filter(Q(host=club_id) | Q(guest=club_id))
    matches = [dict(round = i + 1, row = []) for i in range(rowsMax)]
    players = list(Player.objects.all())
    playersToDisplay = list(Player.objects.all().filter(team=club_id).order_by('first_name'))

    for match in matchesTT:
        host = 0
        guest = 0
        outcome = 0

        eventsTT = list(Event.objects.values_list("event_type", "match", "player").filter(Q(event_type='GOAL') | Q(event_type='GPEN')).filter(match=match.id))

        for event in eventsTT:
            teamId = [player for player in players if player.id == event[2]][0].team.id

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

    return render(request, "club.html", {"team": team, "players": playersToDisplay, "matches": matches, "rowsMax": rowsMax})

def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "player.html", {"player": player})


def players(request):
    playersArray = list(Player.objects.all().order_by('first_name'))

    if request.method == "POST":
        searched = request.POST['searched'].split(" ", 1)
        firstName = ''
        lastName = ''
        i= 0

        for item in searched:
            if i == 0:
                firstName = item
            elif i == 1:
                lastName = item
            i += 1

        playersArray = list(Player.objects.all().filter(first_name__contains=firstName, last_name__contains=lastName).order_by('first_name'))

        return render(request, 'players.html', {'searched':searched,'players': playersArray})

    return render(request, "players.html", {"players": playersArray})


def increment_favourite(request, player_id):
        player = Player.objects.get(pk=player_id)
        player.favourite += 1
        player.save()
        return redirect(request.META['HTTP_REFERER'])
        
def pdf(request, pdf_id): 
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    textobj = c.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont('Helvetica', 14)

    lines = []

    if pdf_id == 1:
        players = Player.objects.all()

        for player in players:
            lines.append("Imie i nazwisko: " + player.first_name + " " + player.last_name)
            lines.append("Klub: " + player.team.name)
            lines.append("Pozycja: " + player.position)
            lines.append("Numer koszulki: " + str(player.shirt_number))
            lines.append("Wysokosc: " + str(player.height) + " cm")
            lines.append("Waga: " + str(player.weight) + " kg")
            lines.append("Polubienia: " + str(player.favourite))
            lines.append(" ")

    counter = 0
    cc = 0

    for line in lines:
        cc = cc + 1
        counter = counter + 1
        textobj.textLine(line)

        if counter > (5 * 8 - 1) and len(lines) != cc:
            c.drawText(textobj)
            c.showPage()
            counter = 0
            textobj = c.beginText()
            textobj.setTextOrigin(inch,inch)
            textobj.setFont('Helvetica', 14)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="Zawodnicy.pdf")