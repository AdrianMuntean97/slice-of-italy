from django.urls import path
from . import views

urlpatterns = [
    path('add_to_bag/', views.add_to_bag, name='add_to_bag'),
    path('', views.bag_view, name='bag'),
    path('adjust_bag/<int:item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove_from_bag/<int:item_id>/', views.remove_from_bag, name='remove_from_bag'),
]
