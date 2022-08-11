from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.cars, name="cars"),
    path('<int:id>', views.car_detail, name='car_detail'),
    path('search', views.search, name='search'),
               ]
