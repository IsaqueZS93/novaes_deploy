from django.urls import path
from .views import list_contracts,create_contract,detail_contract,add_service
urlpatterns=[path('',list_contracts,name='contracts_list'),path('novo/',create_contract,name='contracts_create'),path('<int:pk>/',detail_contract,name='contracts_detail'),path('<int:contract_id>/servicos/novo/',add_service,name='contracts_services_create')]
