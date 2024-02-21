from django.urls import path
from . import views

urlpatterns = [
    path('', views.pizzas, name='pizzas'),
    path('<int:pizza_id>/', views.pizza_detail, name='pizza_detail'),
    path('add/', views.add_pizza, name='add_pizza'),
    path('edit/<int:pizza_id>/', views.edit_pizza, name='edit_pizza'),
    path('delete/<int:pizza_id>/', views.delete_pizza, name='delete_pizza'),
]
