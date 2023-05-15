from django.contrib import admin

# Register your models here.
from .models import Stadium, Team, Player, Match, Event, Change

admin.site.register(Stadium)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Event)
admin.site.register(Change)