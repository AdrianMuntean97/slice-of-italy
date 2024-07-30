from django.db import models
from django.contrib.auth.models import User
from pizzas.models import Pizza

class Review(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.pizza.name}'
