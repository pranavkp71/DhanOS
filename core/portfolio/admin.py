from django.contrib import admin
from .models import Portfolio, Holding, DailySummary

admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(DailySummary)