from django.urls import path
from .views import calendar,create_plan
urlpatterns=[path('',calendar,name='planning_calendar'),path('novo/',create_plan,name='planning_create')]
