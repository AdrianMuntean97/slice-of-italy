from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_pizzas, name='pizzas'),
    path('pizza/<int:pizza_id>/', views.pizzas_detail, name='pizzas_detail'),
]
