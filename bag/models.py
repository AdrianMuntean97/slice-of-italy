from django.db import models
from django.conf import settings
from pizzas.models import Pizza

class Bag(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def grand_total(self):
        return sum(item.subtotal for item in self.bagitem_set.all())


class BagItem(models.Model):
    bag = models.ForeignKey('Bag', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.pizza:  # Check if pizza is not None
            pizza_price = self.pizza.price
            self.subtotal = self.quantity * pizza_price
        super().save(*args, **kwargs)