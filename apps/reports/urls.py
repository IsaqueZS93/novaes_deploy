from django.urls import path
from .views import index,print_report
urlpatterns=[path('',index,name='reports_index'),path('impressao/',print_report,name='reports_print')]
