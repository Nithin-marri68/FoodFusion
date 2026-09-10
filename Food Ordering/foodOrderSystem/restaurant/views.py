from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from restaurant.models import restaurantUser, foodItems
from order.models import Order


def clear_old_messages(request):
    storage = messages.get_messages(request)
    list(storage)


def loginRestaurant(request):

    if request.method == 'POST':

        clear_old_messages(request)

        email = request.POST.get(
            'email',
            ''
        ).strip().lower()

        password = request.POST.get(
            'password',
            ''
        )

        if not email or not password:

            messages.error(
                request,
                'Please enter both email and password.'
            )

            return redirect('loginRestaurant')

        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                'Please enter a valid email address.'
            )

            return redirect('loginRestaurant')

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:

            messages.error(
                request,
                'Invalid email or password.'
            )

            return redirect('loginRestaurant')

        if not user.is_active:

            messages.error(
                request,
                'Your restaurant account is inactive.'
            )

            return redirect('loginRestaurant')

        if not user.is_restaurant:

            messages.error(
                request,
                'This account is registered as a customer.'
            )

            return redirect('loginRestaurant')

        login(
            request,
            user
        )

        messages.success(
            request,
            'Successfully logged in!'
        )

        return redirect('addMenu')

    return render(
        request,
        'loginRestaurant.html'
    )


def registerRestaurant(request):

    if request.method == 'POST':

        restaurantName = request.POST.get(
            'restaurantName',
            ''
        ).strip()

        ownerName = request.POST.get(
            'ownerName',
            ''
        ).strip()

        address = request.POST.get(
            'address',
            ''
        ).strip()

        restaurantContact = request.POST.get(
            'restaurantContact',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip().lower()

        password = request.POST.get(
            'password',
            ''
        )

        # Restaurant name validation
        if not restaurantName:

            messages.error(
                request,
                'Please enter the restaurant name.'
            )

            return redirect('registerRestaurant')

        if len(restaurantName) < 2:

            messages.error(
                request,
                'Restaurant name must contain at least 2 characters.'
            )

            return redirect('registerRestaurant')

        # Owner name validation
        if not ownerName:

            messages.error(
                request,
                'Please enter the owner name.'
            )

            return redirect('registerRestaurant')

        # Address validation
        if len(address) < 10:

            messages.error(
                request,
                'Please enter a complete restaurant address.'
            )

            return redirect('registerRestaurant')

        if len(address) > 500:

            messages.error(
                request,
                'Address cannot exceed 500 characters.'
            )

            return redirect('registerRestaurant')

        # Email validation
        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                'Please enter a valid email address.'
            )

            return redirect('registerRestaurant')

        # Password validation
        if len(password) < 8:

            messages.error(
                request,
                'Password must contain at least 8 characters.'
            )

            return redirect('registerRestaurant')

        # Duplicate email
        if restaurantUser.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                'An account with this email already exists.'
            )

            return redirect('registerRestaurant')

        # Prevent customer and restaurant accounts
        # from using the same email.
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                'An account with this email already exists.'
            )

            return redirect('registerRestaurant')

        try:

            restaurant_data = restaurantUser(

                restaurantName=restaurantName,

                ownerName=ownerName,

                address=address,

                restaurantContact=restaurantContact,

                email=email,

                username=email,

                is_restaurant=True,

                is_user=False,

                password=make_password(password)
            )

            restaurant_data.save()

            messages.success(
                request,
                'Restaurant registered successfully! Please log in.'
            )

            return redirect('loginRestaurant')

        except Exception as error:

            print(
                'Restaurant registration error:',
                error
            )

            messages.error(
                request,
                'Unable to register the restaurant. Please check your details and try again.'
            )

            return redirect('registerRestaurant')

    return render(
        request,
        'registerRestaurant.html'
    )


@login_required
def addMenu(request):

    if not request.user.is_restaurant:

        messages.error(
            request,
            'Please log in as a restaurant.'
        )

        return redirect('loginRestaurant')

    try:

        restaurant = restaurantUser.objects.get(
            email=request.user.email
        )

    except restaurantUser.DoesNotExist:

        messages.error(
            request,
            'Restaurant profile not found.'
        )

        return redirect('loginRestaurant')

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        price = request.POST.get(
            'price',
            ''
        ).strip()

        image = request.FILES.get(
            'image'
        )

        # Food name validation
        if not name:

            messages.error(
                request,
                'Please enter the food name.'
            )

            return redirect('addMenu')

        if len(name) < 2:

            messages.error(
                request,
                'Food name must contain at least 2 characters.'
            )

            return redirect('addMenu')

        if len(name) > 255:

            messages.error(
                request,
                'Food name cannot exceed 255 characters.'
            )

            return redirect('addMenu')

        # Price validation
        if not price:

            messages.error(
                request,
                'Please enter the food price.'
            )

            return redirect('addMenu')

        try:

            price_value = Decimal(price)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                'Please enter a valid price.'
            )

            return redirect('addMenu')

        if price_value <= 0:

            messages.error(
                request,
                'Food price must be greater than zero.'
            )

            return redirect('addMenu')

        if price_value > Decimal('100000'):

            messages.error(
                request,
                'Food price cannot exceed ₹100,000.'
            )

            return redirect('addMenu')

        # Image validation
        if not image:

            messages.error(
                request,
                'Please upload a food image.'
            )

            return redirect('addMenu')

        allowed_types = [
            'image/jpeg',
            'image/png',
            'image/webp'
        ]

        if image.content_type not in allowed_types:

            messages.error(
                request,
                'Only JPG, PNG, and WEBP images are allowed.'
            )

            return redirect('addMenu')

        # 5 MB limit
        if image.size > 5 * 1024 * 1024:

            messages.error(
                request,
                'Image size cannot exceed 5 MB.'
            )

            return redirect('addMenu')

        try:

            foodItems.objects.create(

                name=name,

                price=price_value,

                image=image,

                restaurantName=restaurant.restaurantName
            )

            messages.success(
                request,
                'Food item added successfully!'
            )

        except Exception as error:

            print(
                'Food item error:',
                error
            )

            messages.error(
                request,
                'Error adding the food item. Please try again.'
            )

        return redirect('addMenu')

    items = foodItems.objects.filter(
        restaurantName=restaurant.restaurantName
    )

    context = {
        'name': restaurant.restaurantName,
        'ownerName': restaurant.ownerName,
        'items': items
    }

    return render(
        request,
        'addMenu.html',
        context
    )


@login_required
def restaurant_orders(request):

    if not request.user.is_restaurant:

        messages.error(
            request,
            'Only restaurant accounts can access restaurant orders.'
        )

        return redirect('menu')

    try:

        restaurant = restaurantUser.objects.get(
            email=request.user.email
        )

    except restaurantUser.DoesNotExist:

        messages.error(
            request,
            'Restaurant profile not found.'
        )

        return redirect('loginRestaurant')

    restaurant_name = restaurant.restaurantName

    orders = (
        Order.objects
        .filter(
            items__restaurant_name=restaurant_name
        )
        .distinct()
        .prefetch_related('items')
        .order_by('-created_at')
    )

    restaurant_orders_data = []

    for order in orders:

        restaurant_items = order.items.filter(
            restaurant_name=restaurant_name
        )

        restaurant_total = sum(
            (
                item.subtotal
                for item in restaurant_items
            ),
            Decimal('0.00')
        )

        restaurant_orders_data.append({
            'order': order,
            'items': restaurant_items,
            'total': restaurant_total,
        })

    return render(
        request,
        'restaurant_orders.html',
        {
            'restaurant': restaurant,
            'orders': restaurant_orders_data
        }
    )


@login_required
def update_order_status(
    request,
    order_id
):

    if not request.user.is_restaurant:

        messages.error(
            request,
            'Only restaurant accounts can update orders.'
        )

        return redirect('menu')

    if request.method != 'POST':

        return redirect('restaurant_orders')

    try:

        restaurant = restaurantUser.objects.get(
            email=request.user.email
        )

    except restaurantUser.DoesNotExist:

        messages.error(
            request,
            'Restaurant profile not found.'
        )

        return redirect('loginRestaurant')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    # Verify that this order actually contains
    # an item belonging to the logged-in restaurant.
    restaurant_has_order_item = order.items.filter(
        restaurant_name=restaurant.restaurantName
    ).exists()

    if not restaurant_has_order_item:

        messages.error(
            request,
            'You are not authorized to update this order.'
        )

        return redirect('restaurant_orders')

    new_status = request.POST.get(
        'status',
        ''
    ).strip()

    valid_statuses = [
        choice[0]
        for choice in Order.STATUS_CHOICES
    ]

    if new_status not in valid_statuses:

        messages.error(
            request,
            'Invalid order status.'
        )

        return redirect('restaurant_orders')

    order.status = new_status

    order.save(
        update_fields=[
            'status',
            'updated_at'
        ]
    )

    messages.success(
        request,
        f'Order #{order.id} status updated successfully.'
    )

    return redirect('restaurant_orders')


def logoutRestaurant(request):

    logout(request)

    return redirect('loginRestaurant')