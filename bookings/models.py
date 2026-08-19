from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from cars.models import Car


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date and self.car_id:
            days = (self.end_date - self.start_date).days
            self.total_cost = days * self.car.daily_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car} booked by {self.customer} ({self.start_date} to {self.end_date})"
