from django.contrib import admin
from .models import Pizza, Category

# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Category, CategoryAdmin)