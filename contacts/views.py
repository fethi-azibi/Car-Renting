from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def inquiry(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        car_title = request.POST['car_title']
        city = request.POST['city']
        state = request.POST['state']
        user_id = request.POST['user_id']
        car_id = request.POST['car_id']
        customer_need = request.POST['customer_need']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'error: You already made an inquiry about this car, please wait until we get '
                                        'back to you.')
                return redirect('/cars/'+car_id)

        contact = Contact(car_id=car_id, user_id=user_id, first_name=first_name, last_name=last_name, city=city,
                          state=state, car_title=car_title, email=email, phone=phone, customer_need=customer_need,
                          message=message)
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            'New Car Inquiry',
            'Inquiry request about '+car_title+' has been made',
            'abdouazibi484@gmail.com',
            [admin_email, ],
            fail_silently=False,
        )
        contact.save()
        messages.success(request, 'Your request has been successfully submitted, we will contact you soon')
        return redirect('/cars/'+car_id)

