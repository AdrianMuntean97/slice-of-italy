from django.db import models
from django.conf import settings
from pizzas.models import Pizza

class Bag(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class BagItem(models.Model):
    bag = models.ForeignKey(Bag, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
