from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'delivery_cost', 'order_total', 'grand_total', 'original_bag', 'stripe_pid')
    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county', 'delivery_cost', 'order_total', 'grand_total', 'original_bag', 'stripe_pid')
    list_display = ('order_number', 'date', 'full_name', 'order_total', 'delivery_cost', 'grand_total',)
    ordering = ('-date',)

    def has_add_permission(self, request):
        return False

admin.site.register(Order, OrderAdmin)
