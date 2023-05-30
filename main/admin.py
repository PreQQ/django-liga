from django.contrib import admin

# Register your models here.
from .models import Stadium, Team, Player, Match, Event, Change



class MatchAdmin(admin.ModelAdmin):
    list_display = ('host', 'guest', 'match_round', 'date')
    list_display_links = ('host', 'guest')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'player', 'minute', 'match')
    list_display_links = ('event_type', 'player')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team')
    list_display_links = ('first_name', 'last_name', 'team')

admin.site.register(Stadium)
admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Change)


