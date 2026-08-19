from django.db import models


class Car(models.Model):
    class Category(models.TextChoices):
        ECONOMY = "economy", "Economy"
        SUV = "suv", "SUV"
        LUXURY = "luxury", "Luxury"
        VAN = "van", "Van"

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.ECONOMY)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.PositiveSmallIntegerField(default=4)
    transmission = models.CharField(
        max_length=10,
        choices=[("automatic", "Automatic"), ("manual", "Manual")],
        default="automatic",
    )
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cars/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
