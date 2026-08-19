from django.shortcuts import render, get_object_or_404
from .models import Car


def car_list(request):
    cars = Car.objects.filter(is_available=True)

    category = request.GET.get("category")
    location = request.GET.get("location")
    q = request.GET.get("q")

    if category:
        cars = cars.filter(category=category)
    if location:
        cars = cars.filter(location__icontains=location)
    if q:
        cars = cars.filter(make__icontains=q) | cars.filter(model__icontains=q)

    context = {
        "cars": cars,
        "categories": Car.Category.choices,
        "selected_category": category or "",
        "location_query": location or "",
        "search_query": q or "",
    }
    return render(request, "cars/car_list.html", context)


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "cars/car_detail.html", {"car": car})
