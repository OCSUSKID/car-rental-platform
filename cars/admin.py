from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "year", "category", "daily_rate", "location", "is_available")
    list_filter = ("category", "transmission", "is_available", "location")
    search_fields = ("make", "model", "location")
