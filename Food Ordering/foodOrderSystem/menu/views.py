from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count

from restaurant.models import foodItems, restaurantUser


@login_required
def menu(request):

    user = request.user

    query = request.GET.get('q', '').strip()
    selected_restaurant = request.GET.get('restaurant', '').strip()

    foods = foodItems.objects.annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    # Search food items
    if query:
        foods = foods.filter(
            Q(name__icontains=query)
        )

    # Filter by restaurant
    if selected_restaurant:
        foods = foods.filter(
            restaurantName=selected_restaurant
        )

    # Get customer name
    if hasattr(user, 'customeruser'):
        name = user.customeruser.name
    else:
        name = "Customer"

    # Initialize cart
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart_empty = len(
        request.session.get('cart', {})
    ) == 0

    # Add item to cart
    if request.method == 'POST':

        item_id = request.POST.get("id")

        if item_id:

            cart = request.session.get(
                'cart',
                {}
            )

            if item_id in cart:

                cart[item_id] += 1

            else:

                cart[item_id] = 1

            request.session['cart'] = cart
            request.session.modified = True

        return render(
            request,
            'index1.html',
            {
                'name': name,
                'foodItems': foods,
                'cart': request.session.get('cart', {}),
                'Empty': cart_empty,
                'restaurant_list': restaurantUser.objects.all(),
                'selected_restaurant': selected_restaurant,
                'search_query': query,
            }
        )

    return render(
        request,
        'index1.html',
        {
            'name': name,
            'foodItems': foods,
            'cart': request.session.get('cart', {}),
            'Empty': cart_empty,
            'restaurant_list': restaurantUser.objects.all(),
            'selected_restaurant': selected_restaurant,
            'search_query': query,
        }
    )


def restaurantPage(request):

    restaurant_name = request.GET.get(
        'restaurant',
        ''
    ).strip()

    foods = foodItems.objects.annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    if restaurant_name:

        foods = foods.filter(
            restaurantName=restaurant_name
        )

    return render(
        request,
        'index1.html',
        {
            'foodItems': foods,
            'restaurant_list': restaurantUser.objects.all(),
            'selected_restaurant': restaurant_name,
            'search_query': '',
        }
    )