from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)


class customerUser(CustomUser):
    name = models.CharField(max_length=50)


class Feedback(models.Model):
    stars = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"{self.stars} Star Feedback"


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.TextField()

    def __str__(self):
        return self.name


class FoodReview(models.Model):
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='food_reviews'
    )

    food = models.ForeignKey(
        'restaurant.foodItems',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.food.name} - {self.rating}/5"