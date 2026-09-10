from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Sum, Count

from customer.models import customerUser, Feedback, Contact, FoodReview
from restaurant.models import restaurantUser, foodItems
from order.models import Order, OrderItem


@staff_member_required
def admin_dashboard(request):

    # =========================
    # BASIC COUNTS
    # =========================

    total_customers = customerUser.objects.filter(
        is_user=True
    ).count()

    total_restaurants = restaurantUser.objects.filter(
        is_restaurant=True
    ).count()

    total_food_items = foodItems.objects.count()

    total_reviews = FoodReview.objects.count()

    total_feedback = Feedback.objects.count()

    total_contacts = Contact.objects.count()

    total_orders = Order.objects.count()


    # =========================
    # REVENUE
    # =========================

    total_revenue = Order.objects.filter(
        status__in=[
            'PLACED',
            'CONFIRMED',
            'PREPARING',
            'OUT_FOR_DELIVERY',
            'DELIVERED'
        ]
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0


    # =========================
    # AVERAGE RATING
    # =========================

    average_rating = FoodReview.objects.aggregate(
        average=Avg('rating')
    )['average']

    if average_rating is None:
        average_rating = 0


    # =========================
    # ORDER STATUS
    # =========================

    order_status_data = []

    for status_code, status_name in Order.STATUS_CHOICES:

        count = Order.objects.filter(
            status=status_code
        ).count()

        order_status_data.append({
            'status': status_name,
            'count': count
        })


    # =========================
    # RATING DISTRIBUTION
    # =========================

    rating_distribution = []

    for rating in range(5, 0, -1):

        count = FoodReview.objects.filter(
            rating=rating
        ).count()

        rating_distribution.append({
            'rating': rating,
            'count': count
        })


    # =========================
    # RESTAURANT PERFORMANCE
    # =========================

    restaurant_data = []

    restaurants = restaurantUser.objects.filter(
        is_restaurant=True
    ).order_by('restaurantName')


    for restaurant in restaurants:

        food_count = foodItems.objects.filter(
            restaurantName=restaurant.restaurantName
        ).count()

        restaurant_orders = Order.objects.filter(
            items__restaurant_name=restaurant.restaurantName
        ).distinct().count()

        restaurant_revenue = OrderItem.objects.filter(
            restaurant_name=restaurant.restaurantName
        ).aggregate(
            total=Sum('subtotal')
        )['total'] or 0

        restaurant_data.append({
            'name': restaurant.restaurantName,
            'food_count': food_count,
            'orders': restaurant_orders,
            'revenue': restaurant_revenue
        })


    # =========================
    # TOP FOOD ITEMS
    # =========================

    top_foods = []

    foods = foodItems.objects.annotate(
        review_average=Avg('reviews__rating'),
        review_count=Count('reviews'),
        order_count=Count('order_items')
    ).order_by(
        '-order_count'
    )[:5]


    for food in foods:

        top_foods.append({
            'name': food.name,
            'restaurant': food.restaurantName,
            'orders': food.order_count,
            'rating': round(
                food.review_average, 1
            ) if food.review_average else 0
        })


    # =========================
    # RECENT ORDERS
    # =========================

    recent_orders = Order.objects.select_related(
        'customer'
    ).prefetch_related(
        'items'
    ).order_by(
        '-created_at'
    )[:5]


    # =========================
    # RECENT REVIEWS
    # =========================

    recent_reviews = (
        FoodReview.objects
        .select_related(
            'customer',
            'food'
        )
        .order_by(
            '-created_at'
        )[:5]
    )


    # =========================
    # CONTEXT
    # =========================

    context = {

        'total_customers': total_customers,

        'total_restaurants': total_restaurants,

        'total_food_items': total_food_items,

        'total_reviews': total_reviews,

        'total_feedback': total_feedback,

        'total_contacts': total_contacts,

        'total_orders': total_orders,

        'total_revenue': total_revenue,

        'average_rating': round(
            average_rating,
            1
        ),

        'rating_distribution':
            rating_distribution,

        'order_status_data':
            order_status_data,

        'restaurant_data':
            restaurant_data,

        'top_foods':
            top_foods,

        'recent_orders':
            recent_orders,

        'recent_reviews':
            recent_reviews,
    }


    return render(
        request,
        'admin_dashboard.html',
        context
    )