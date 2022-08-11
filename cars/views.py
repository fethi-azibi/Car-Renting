from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from cars.models import Car


# Create your views here.
def cars(request):
    cars = Car.objects.order_by("-created_date")
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'cars': paged_cars,
        'body_style_search': body_style_search,
        'year_search': year_search,
        'city_search': city_search,
        'model_search': model_search,
    }

    return render(request, 'cars/cars.html', data)


def car_detail(request, id):
    single_car = get_object_or_404(Car, pk=id)
    data = {
        'single_car': single_car,
    }
    return render(request, 'cars/car_detail.html', data)


def search(request):
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()
    cars = Car.objects.order_by('-created_date')
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            cars = cars.filter(description__icontains=keyword)
    if 'model' in request.GET:
        model = request.GET.get('model')
        if model:
            cars = cars.filter(model__iexact=model)
    if 'year' in request.GET:
        year = request.GET.get('year')
        if year:
            cars = cars.filter(year__iexact=year)
    if 'city' in request.GET:
        city = request.GET.get('city')
        if city:
            cars = cars.filter(city__iexact=city)
    if 'body_style' in request.GET:
        body_style = request.GET.get('body_style')
        if body_style:
            cars = cars.filter(body_style__icontains=body_style)
    if 'min_price' in request.GET:
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if max_price:
            cars = cars.filter(price__lte=max_price, price__gte=min_price)



    data = {
        'cars': cars,
        'body_style_search': body_style_search,
        'year_search': year_search,
        'city_search': city_search,
        'model_search': model_search,
        'transmission_search': transmission_search,
    }
    return render(request, 'cars/search.html', data)
