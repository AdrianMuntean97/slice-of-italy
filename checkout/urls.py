from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('process_checkout/', views.process_checkout, name='process_checkout'),
]