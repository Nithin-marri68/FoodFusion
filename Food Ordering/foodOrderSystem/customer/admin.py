from django.contrib import admin
from customer.models import (
    customerUser,
    Feedback,
    Contact,
    FoodReview
)


# =========================
# CUSTOMER ADMIN
# =========================

@admin.register(customerUser)
class CustomerUserAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'is_user',
        'is_restaurant',
        'is_active',
        'date_joined',
    )

    list_filter = (
        'is_user',
        'is_restaurant',
        'is_active',
    )

    search_fields = (
        'name',
        'email',
        'username',
    )

    ordering = (
        '-date_joined',
    )

    readonly_fields = (
        'date_joined',
        'last_login',
    )


# =========================
# FEEDBACK ADMIN
# =========================

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'stars',
        'comments',
    )

    list_filter = (
        'stars',
    )

    search_fields = (
        'comments',
    )

    ordering = (
        '-id',
    )


# =========================
# CONTACT ADMIN
# =========================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'subject',
    )

    search_fields = (
        'name',
        'email',
        'subject',
    )

    ordering = (
        '-id',
    )


# =========================
# FOOD REVIEW ADMIN
# =========================

@admin.register(FoodReview)
class FoodReviewAdmin(admin.ModelAdmin):

    list_display = (
        'food',
        'customer',
        'rating',
        'comment',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'food__name',
        'customer__username',
        'customer__email',
        'comment',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )