from django.db import models
from django.conf import settings
from restaurant.models import foodItems


class Order(models.Model):

    STATUS_CHOICES = [
        ('PLACED', 'Order Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()

    delivery_address = models.TextField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='PLACED'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    food = models.ForeignKey(
        foodItems,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    food_name = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    restaurant_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.food_name} x {self.quantity}"