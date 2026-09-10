from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'food_name',
        'quantity',
        'price',
        'subtotal',
        'restaurant_name',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'customer_email',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'customer_email',
        'delivery_address',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'food_name',
        'order',
        'quantity',
        'price',
        'subtotal',
        'restaurant_name',
    )

    list_filter = (
        'restaurant_name',
    )

    search_fields = (
        'food_name',
        'restaurant_name',
    )