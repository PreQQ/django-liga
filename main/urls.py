from django.contrib import admin
from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.matches, name="index"),
    # path("matches/", views.matches, name="matches"),
    path("match/<int:match_id>", views.match, name="match"),
    path("table/", views.table, name="table"),
    path("statistics/", views.statistics, name="statistics"),
    path("player/<int:player_id>", views.player, name="player"),
    path("club/<int:club_id>", views.club, name="club"),
]