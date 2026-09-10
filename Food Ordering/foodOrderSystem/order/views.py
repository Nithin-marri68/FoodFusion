from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from restaurant.models import foodItems
from order.models import Order, OrderItem


MAX_ITEM_QUANTITY = 20


def get_valid_cart(request):
    """
    Clean invalid cart entries and return a safe cart dictionary.
    """

    session_cart = request.session.get('cart', {})

    if not isinstance(session_cart, dict):
        session_cart = {}

    valid_cart = {}

    for item_id, quantity in session_cart.items():

        try:
            item_id = str(int(item_id))
            quantity = int(quantity)

        except (TypeError, ValueError):
            continue

        if quantity < 1:
            continue

        if quantity > MAX_ITEM_QUANTITY:
            quantity = MAX_ITEM_QUANTITY

        if not foodItems.objects.filter(id=item_id).exists():
            continue

        valid_cart[item_id] = quantity

    request.session['cart'] = valid_cart
    request.session.modified = True

    return valid_cart


def build_cart_details(request):
    """
    Build cart details using the current database prices.
    """

    cart = get_valid_cart(request)

    cart_details = {}
    total_cost = Decimal('0.00')

    for item_id, quantity in cart.items():

        try:
            item = foodItems.objects.get(id=item_id)

        except foodItems.DoesNotExist:
            continue

        subtotal = item.price * quantity

        total_cost += subtotal

        cart_details[item_id] = {
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal,
        }

    return cart_details, total_cost


@login_required
def Cart(request):

    cart = get_valid_cart(request)

    if request.method == 'POST':

        action = request.POST.get('action')
        item_id = request.POST.get('item_id')

        if item_id:

            try:
                item_id = str(int(item_id))

            except (TypeError, ValueError):

                messages.error(
                    request,
                    'Invalid food item.'
                )

                return redirect('cart')

            if not foodItems.objects.filter(
                id=item_id
            ).exists():

                messages.error(
                    request,
                    'Food item no longer exists.'
                )

                cart.pop(item_id, None)

            elif action == 'add':

                current_quantity = cart.get(
                    item_id,
                    0
                )

                if current_quantity >= MAX_ITEM_QUANTITY:

                    messages.warning(
                        request,
                        f'Maximum quantity is {MAX_ITEM_QUANTITY} per item.'
                    )

                else:

                    cart[item_id] = current_quantity + 1

            elif action == 'increment':

                if item_id in cart:

                    if cart[item_id] >= MAX_ITEM_QUANTITY:

                        messages.warning(
                            request,
                            f'Maximum quantity is {MAX_ITEM_QUANTITY} per item.'
                        )

                    else:

                        cart[item_id] += 1

            elif action == 'decrement':

                if item_id in cart:

                    cart[item_id] -= 1

                    if cart[item_id] <= 0:

                        cart.pop(item_id, None)

            elif action == 'remove':

                cart.pop(
                    item_id,
                    None
                )

            else:

                messages.error(
                    request,
                    'Invalid cart action.'
                )

        request.session['cart'] = cart
        request.session.modified = True

        return redirect('cart')

    cart_details, total_cost = build_cart_details(
        request
    )

    return render(
        request,
        'cart.html',
        {
            'cart': cart_details,
            'totalCost': total_cost,
        }
    )


@login_required
def checkout(request):

    cart_details, total_cost = build_cart_details(
        request
    )

    if not cart_details:

        messages.warning(
            request,
            'Your cart is empty.'
        )

        return redirect('cart')

    if request.method == 'POST':

        delivery_address = request.POST.get(
            'delivery_address',
            ''
        ).strip()

        if not delivery_address:

            messages.error(
                request,
                'Please enter your delivery address.'
            )

            return render(
                request,
                'checkout.html',
                {
                    'cart': cart_details,
                    'totalCost': total_cost,
                    'delivery_address':
                        delivery_address,
                }
            )

        if len(delivery_address) < 10:

            messages.error(
                request,
                'Please enter a complete delivery address.'
            )

            return render(
                request,
                'checkout.html',
                {
                    'cart': cart_details,
                    'totalCost': total_cost,
                    'delivery_address':
                        delivery_address,
                }
            )

        if len(delivery_address) > 500:

            messages.error(
                request,
                'Delivery address cannot exceed 500 characters.'
            )

            return render(
                request,
                'checkout.html',
                {
                    'cart': cart_details,
                    'totalCost': total_cost,
                    'delivery_address':
                        delivery_address,
                }
            )

        # Recalculate everything immediately
        # before creating the order.
        cart_details, total_cost = build_cart_details(
            request
        )

        if not cart_details:

            messages.warning(
                request,
                'Your cart is empty.'
            )

            return redirect('cart')

        customer_name = request.user.get_full_name().strip()

        if not customer_name:

            if hasattr(
                request.user,
                'customeruser'
            ):

                customer_name = (
                    request.user.customeruser.name
                )

            else:

                customer_name = request.user.username

        try:

            with transaction.atomic():

                order = Order.objects.create(

                    customer=request.user,

                    customer_name=customer_name,

                    customer_email=request.user.email,

                    delivery_address=delivery_address,

                    total_amount=total_cost,

                    status='PLACED',
                )

                for item_id, details in cart_details.items():

                    item = details['item']

                    quantity = details['quantity']

                    subtotal = details['subtotal']

                    OrderItem.objects.create(

                        order=order,

                        food=item,

                        food_name=item.name,

                        quantity=quantity,

                        price=item.price,

                        subtotal=subtotal,

                        restaurant_name=item.restaurantName,
                    )

        except Exception as error:

            print(
                'Order creation error:',
                error
            )

            messages.error(
                request,
                'Unable to place your order. Please try again.'
            )

            return redirect('checkout')

        # Clear cart only after successful order creation.
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(
            request,
            f'Order #{order.id} has been placed successfully!'
        )

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'checkout.html',
        {
            'cart': cart_details,
            'totalCost': total_cost,
        }
    )


@login_required
def order_success(
    request,
    order_id
):

    order = (
        Order.objects
        .filter(
            id=order_id,
            customer=request.user
        )
        .prefetch_related('items')
        .first()
    )

    if order is None:

        messages.error(
            request,
            'Order not found.'
        )

        return redirect('menu')

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )


@login_required
def order_history(request):

    orders = (
        Order.objects
        .filter(
            customer=request.user
        )
        .prefetch_related('items')
        .order_by('-created_at')
    )

    return render(
        request,
        'order_history.html',
        {
            'orders': orders
        }
    )