from django.contrib import admin

from restaurant.models import restaurantUser, foodItems


# =========================================================
# RESTAURANT ADMIN
# =========================================================

@admin.register(restaurantUser)
class RestaurantUserAdmin(admin.ModelAdmin):

    list_display = (
        'restaurantName',
        'ownerName',
        'email',
        'restaurantContact',
        'is_restaurant',
        'is_active',
    )

    list_filter = (
        'is_restaurant',
        'is_active',
    )

    search_fields = (
        'restaurantName',
        'ownerName',
        'email',
        'address',
    )

    ordering = (
        'restaurantName',
    )


# =========================================================
# FOOD ITEM ADMIN
# =========================================================

@admin.register(foodItems)
class FoodItemsAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'restaurantName',
        'price',
        'image',
    )

    list_filter = (
        'restaurantName',
    )

    search_fields = (
        'name',
        'restaurantName',
    )

    ordering = (
        'restaurantName',
        'name',
    )