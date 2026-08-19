from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("car", "customer", "start_date", "end_date", "status", "total_cost")
    list_filter = ("status",)
    search_fields = ("car__make", "car__model", "customer__username")
