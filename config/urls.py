from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('admin/',admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',include('apps.dashboards.urls')),
    path('clientes/',include('apps.clients.urls')),
    path('contratos/',include('apps.contracts.urls')),
    path('equipes/',include('apps.teams.urls')),
    path('planejamento/',include('apps.planning.urls')),
    path('execucao/',include('apps.execution.urls')),
    path('financeiro/',include('apps.finance.urls')),
    path('relatorios/',include('apps.reports.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
