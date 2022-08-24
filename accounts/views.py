from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from contacts.models import Contact
# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, "You are logged in now.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email Already Exists")
                else:
                    user = User.objects.create(last_name=last_name, first_name=first_name, username=username, email=email, password=password)
                    user.save()
                    auth.login(request, user)
                    messages.success(request, 'you are now logged in.')
                    return redirect('dashboard')
        else:
            messages.error(request, "passwords does not match")
    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'user_inquiry': user_inquiry
    }
    return render(request, 'accounts/dashboard.html', data)


def logout(request):
    """ if request.user.is_authenticated:
        auth.logout(request) """
    if request.method == "POST":
        auth.logout(request)
        #messages.success(request, "You are successfully logged out.")
        return redirect('home')
    return redirect('home')
