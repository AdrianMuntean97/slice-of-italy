from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pizza_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:pizza_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('', views.wishlist_view, name='wishlist'),
]
