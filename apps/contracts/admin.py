from django.contrib import admin
from .models import Contract,ContractService,ServiceCategory
admin.site.register([Contract,ContractService,ServiceCategory])
