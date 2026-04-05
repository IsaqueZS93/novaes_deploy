from django.urls import path
from .views import list_teams,create_team
urlpatterns=[path('',list_teams,name='teams_list'),path('novo/',create_team,name='teams_create')]
