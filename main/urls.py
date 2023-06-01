from django.contrib import admin
from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.matches, name="index"),
    path("players/", views.players, name="players"),
    path("match/<int:match_id>", views.match, name="match"),
    path("table/", views.table, name="table"),
    path("statistics/", views.statistics, name="statistics"),
    path("player/<int:player_id>", views.player, name="player"),
    path("club/<int:club_id>", views.club, name="club"),
    path('increment_favourite/<int:player_id>/', views.increment_favourite, name='increment_favourite'),
    path('pdf/<int:pdf_id>/', views.pdf, name='pdf'),
]