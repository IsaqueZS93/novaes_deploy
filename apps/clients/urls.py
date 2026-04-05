from django.urls import path
from .views import list_clients,create_client,edit_client
urlpatterns=[path('',list_clients,name='clients_list'),path('novo/',create_client,name='clients_create'),path('<int:pk>/editar/',edit_client,name='clients_edit')]
