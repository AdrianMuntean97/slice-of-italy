from django.db import models
from django.contrib.auth.models import User
from pizzas.models import Pizza

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    pizzas = models.ManyToManyField(Pizza, related_name='wishlisted_by')

    def __str__(self):
        return f'{self.user.username} Wishlist'
