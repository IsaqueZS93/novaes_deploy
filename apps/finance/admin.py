from django.contrib import admin
from .models import CostCategory,CostExpense,Revenue
admin.site.register([CostCategory,CostExpense,Revenue])
