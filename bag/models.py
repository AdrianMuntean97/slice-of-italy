from django.db import models
from django.conf import settings
from pizzas.models import Pizza

class Bag(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Pizza, through='BagItem')
    
    def grand_total(self):
        return sum(item.subtotal for item in self.order_items.all())

class OrderItem(models.Model):
    bag = models.ForeignKey(Bag, related_name='order_items', on_delete=models.CASCADE)

class BagItem(models.Model):
    bag = models.ForeignKey(Bag, related_name='bag_items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.pizza and not self.pk:  # Check if pizza is not None and it's a new instance
            self.price = self.pizza.price
        self.update_subtotal()
        super().save(*args, **kwargs)

    def update_subtotal(self):
        self.subtotal = self.quantity * self.price

