from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_pizzas, name='pizzas'),
]