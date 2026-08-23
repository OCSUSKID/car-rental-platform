from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from cars.models import Car
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id, is_available=True)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.customer = request.user
            try:
                booking.full_clean()
            except ValidationError as error:
                form.add_error(None, error)
            else:
                booking.save()
                messages.success(request, "Booking created! It's pending confirmation.")
                return redirect("bookings:my_bookings")
    else:
        form = BookingForm()

    return render(request, "bookings/create_booking.html", {"form": form, "car": car})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.status == Booking.Status.PENDING:
        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect("bookings:my_bookings")
