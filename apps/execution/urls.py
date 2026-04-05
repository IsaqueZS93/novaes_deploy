from django.urls import path
from .views import list_execution,create_execution
urlpatterns=[path('',list_execution,name='execution_list'),path('novo/',create_execution,name='execution_create')]
