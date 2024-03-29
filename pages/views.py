from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Team
from cars.models import Car


# Create your views here.
def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by("-created_date")
    # search_fields = Car.objects.values('model', 'year', 'body_style', 'city')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'body_style_search': body_style_search,
        'year_search': year_search,
        'city_search': city_search,
        'model_search': model_search,
        # 'search_fields':search_fields,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)


def services(request):
    return render(request, 'pages/services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            'New Email from Car Selling: '+subject,
            'Name: '+name+' Email: '+email+'phone: '+phone+'message: '+message,
            'abdouazibi484@gmail.com',
            [admin_email, ],
            fail_silently=False,
        )
        messages.success(request, 'Your request has been successfully submitted, we will contact you soon')
        return redirect('contact')

    return render(request, 'pages/contact.html')
