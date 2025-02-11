from django.contrib import admin
from main_app.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'owner']