from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cars.models import Car
from .models import Booking


class BookingFlowTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="customer", password="password123")
		self.car = Car.objects.create(
			make="Toyota",
			model="Corolla",
			year=2024,
			daily_rate="45.00",
			location="Downtown",
		)
		self.client.force_login(self.user)

	def booking_dates(self):
		return {
			"start_date": date.today() + timedelta(days=1),
			"end_date": date.today() + timedelta(days=4),
		}

	def test_booking_calculates_total_cost(self):
		response = self.client.post(
			reverse("bookings:create_booking", args=[self.car.pk]), self.booking_dates()
		)

		self.assertRedirects(response, reverse("bookings:my_bookings"))
		self.assertEqual(Booking.objects.get().total_cost, Decimal("135.00"))

	def test_overlapping_booking_is_rejected(self):
		Booking.objects.create(customer=self.user, car=self.car, **self.booking_dates())
		dates = self.booking_dates()
		dates["start_date"] += timedelta(days=1)
		dates["end_date"] += timedelta(days=1)

		response = self.client.post(
			reverse("bookings:create_booking", args=[self.car.pk]), dates
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Booking.objects.count(), 1)
		self.assertContains(response, "already booked")

	def test_cancellation_requires_post(self):
		booking = Booking.objects.create(customer=self.user, car=self.car, **self.booking_dates())

		response = self.client.get(reverse("bookings:cancel_booking", args=[booking.pk]))

		self.assertEqual(response.status_code, 405)
		booking.refresh_from_db()
		self.assertEqual(booking.status, Booking.Status.PENDING)
