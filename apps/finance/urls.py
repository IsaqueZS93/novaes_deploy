from django.urls import path
from .views import costs_list,costs_create,revenues_list,revenues_create
urlpatterns=[
 path('custos/',costs_list,name='finance_costs_list'),path('custos/novo/',costs_create,name='finance_costs_create'),
 path('receitas/',revenues_list,name='finance_revenues_list'),path('receitas/nova/',revenues_create,name='finance_revenues_create')]
