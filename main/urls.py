from django.contrib import admin
from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.views, name="index"),
    path("matches/", views.matches, name="matches"),
    path("<int:match_id>", views.match, name="match"),
    path("table/", views.table, name="table"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:team_id>", views.club, name="club"),
    path("<int:player_id>", views.player, name="player"),
]