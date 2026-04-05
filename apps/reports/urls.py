from django.urls import path
from .views import export_csv, index

urlpatterns = [
    path('', index, name='reports_index'),
    path('export/csv/', export_csv, name='reports_export_csv'),
]
