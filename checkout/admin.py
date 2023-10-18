# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd Party
from django.contrib import admin
from django.contrib import admin
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from .models import Order, OrderLineItem
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class OrderLineItemAdminInline(admin.TabularInline):
    """
    A class to register OrderInlineItem model in admin panel
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    A class to register Order model in admin panel
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid'
    )
    fields = (
        'order_number',
        'date',
        'full_name',
        'email',
        'phone_number',
        'address1',
        'address2',
        'town_or_city',
        'postcode',
        'county',
        'country',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid'
    )
    list_display = (
        'order_number',
        'date',
        'user_profile',
        'full_name',
        'delivery_cost',
        'order_total',
        'grand_total',
    )
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
