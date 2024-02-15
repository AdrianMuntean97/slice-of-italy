from django.db import models
from django.conf import settings
from bag.models import BagItem

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_number = models.CharField(max_length=32, null=False, editable=False)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    bag_item = models.OneToOneField(BagItem, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)
