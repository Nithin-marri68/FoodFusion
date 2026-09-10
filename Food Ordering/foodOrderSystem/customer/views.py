from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count

from customer.models import customerUser, Feedback, Contact, FoodReview
from restaurant.models import foodItems


User = get_user_model()


def loginUser(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(
                request,
                'Please enter both email and password.'
            )
            return redirect('login')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                'Please enter a valid email address.'
            )
            return redirect('login')

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            messages.error(
                request,
                'Invalid email or password.'
            )
            return redirect('login')

        if not user.is_active:
            messages.error(
                request,
                'Your account is inactive.'
            )
            return redirect('login')

        if user.is_restaurant:
            messages.error(
                request,
                'This account is registered as a restaurant.'
            )
            return redirect('login')

        login(request, user)

        messages.success(
            request,
            'Successfully logged in!'
        )

        return redirect('menu')

    return render(
        request,
        'authentication/login.html'
    )


def registerUser(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        # Name validation
        if not name:

            messages.error(
                request,
                'Please enter your name.'
            )

            return redirect('register')

        if len(name) < 2:

            messages.error(
                request,
                'Name must contain at least 2 characters.'
            )

            return redirect('register')

        # Email validation
        try:
            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                'Please enter a valid email address.'
            )

            return redirect('register')

        # Password validation
        if len(password) < 8:

            messages.error(
                request,
                'Password must contain at least 8 characters.'
            )

            return redirect('register')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        # Existing account validation
        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                'An account with this email already exists.'
            )

            return redirect('register')

        try:

            user = customerUser.objects.create(
                name=name,
                email=email,
                username=email,
                password=make_password(password),
                is_user=True,
                is_restaurant=False
            )

            messages.success(
                request,
                'Registration successful! Please log in.'
            )

            return redirect('login')

        except Exception as error:

            print(
                'Customer registration error:',
                error
            )

            messages.error(
                request,
                'Something went wrong. Please try again.'
            )

            return redirect('register')

    return render(
        request,
        'authentication/register.html'
    )


def forgetPassword(request):

    return render(
        request,
        'authentication/forgetPassword.html'
    )


def logoutUser(request):

    logout(request)

    return render(
        request,
        'authentication/logout.html'
    )


def feedback_form(request):

    if request.method == 'POST':

        comments = request.POST.get(
            'comment',
            ''
        ).strip()

        if not comments:

            messages.error(
                request,
                'Please enter your feedback.'
            )

            return redirect('feedback_form')

        try:

            Feedback.objects.create(
                stars=0,
                comments=comments
            )

            return render(
                request,
                'thank_you.html'
            )

        except Exception:

            return HttpResponse(
                '<h1>Sorry!</h1>'
                '<p>There is an issue processing your feedback.</p>'
            )

    return render(
        request,
        'feedback.html'
    )


def index(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip().lower()

        subject = request.POST.get(
            'subject',
            ''
        ).strip()

        if not name or not email or not subject:

            messages.error(
                request,
                'Please complete all contact fields.'
            )

            return redirect('index')

        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                'Please enter a valid email address.'
            )

            return redirect('index')

        try:

            Contact.objects.create(
                name=name,
                email=email,
                subject=subject
            )

            return render(
                request,
                'thank_you.html'
            )

        except Exception:

            return HttpResponse(
                '<h1>Sorry!</h1>'
                '<p>There is an issue processing your request.</p>'
            )

    return render(
        request,
        'contact.html'
    )


def Home(request):

    return render(
        request,
        'home.html'
    )


@login_required
def add_review(request, food_id):

    food = get_object_or_404(
        foodItems,
        id=food_id
    )

    # Restaurant accounts cannot review food
    if request.user.is_restaurant:

        messages.error(
            request,
            'Restaurant accounts cannot submit food reviews.'
        )

        return redirect('menu')

    if request.method == 'POST':

        rating = request.POST.get(
            'rating'
        )

        comment = request.POST.get(
            'comment',
            ''
        ).strip()

        try:

            rating = int(rating)

        except (TypeError, ValueError):

            messages.error(
                request,
                'Please select a valid rating.'
            )

            return redirect(
                'add_review',
                food_id=food.id
            )

        if rating < 1 or rating > 5:

            messages.error(
                request,
                'Rating must be between 1 and 5 stars.'
            )

            return redirect(
                'add_review',
                food_id=food.id
            )

        if len(comment) > 1000:

            messages.error(
                request,
                'Review comment cannot exceed 1000 characters.'
            )

            return redirect(
                'add_review',
                food_id=food.id
            )

        review, created = FoodReview.objects.update_or_create(

            customer=request.user,

            food=food,

            defaults={
                'rating': rating,
                'comment': comment
            }
        )

        if created:

            messages.success(
                request,
                'Your review has been submitted successfully!'
            )

        else:

            messages.success(
                request,
                'Your review has been updated successfully!'
            )

        return redirect(
            'add_review',
            food_id=food.id
        )

    reviews = (
        FoodReview.objects
        .filter(food=food)
        .select_related('customer')
    )

    try:

        customer_review = FoodReview.objects.get(
            customer=request.user,
            food=food
        )

    except FoodReview.DoesNotExist:

        customer_review = None

    return render(
        request,
        'review.html',
        {
            'food': food,
            'reviews': reviews,
            'customer_review': customer_review
        }
    )