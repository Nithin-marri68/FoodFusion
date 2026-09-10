from django.contrib import admin
from django.urls import path

from customer import views as customerviews
from customer import admin_views

from menu import views as menuviews
from order import views as orderviews
from restaurant import views as restaurantviews

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'admin-dashboard/',
        admin_views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'login/',
        customerviews.loginUser,
        name='login'
    ),

    path(
        'logout/',
        customerviews.logoutUser,
        name='logout'
    ),

    path(
        'register/',
        customerviews.registerUser,
        name='register'
    ),

    path(
        'forgetPassword/',
        customerviews.forgetPassword,
        name='forgetPassword'
    ),

    path(
        'loginRestaurant/',
        restaurantviews.loginRestaurant,
        name='loginRestaurant'
    ),

    path(
        'registerRestaurant/',
        restaurantviews.registerRestaurant,
        name='registerRestaurant'
    ),

    path(
        'logoutRestaurant/',
        restaurantviews.logoutRestaurant,
        name='logoutR'
    ),

    path(
        'menu/',
        menuviews.menu,
        name='menu'
    ),

    path(
        'restaurantPage/',
        menuviews.restaurantPage,
        name='restaurantPage'
    ),

    path(
        'addMenu/',
        restaurantviews.addMenu,
        name='addMenu'
    ),

    path(
        'restaurant-orders/',
        restaurantviews.restaurant_orders,
        name='restaurant_orders'
    ),

    path(
        'restaurant-orders/<int:order_id>/status/',
        restaurantviews.update_order_status,
        name='update_order_status'
    ),

    path(
        'cart/',
        orderviews.Cart,
        name='cart'
    ),

    path(
        'checkout/',
        orderviews.checkout,
        name='checkout'
    ),

    path(
        'order-success/<int:order_id>/',
        orderviews.order_success,
        name='order_success'
    ),

    path(
        'orders/',
        orderviews.order_history,
        name='order_history'
    ),

    path(
        'feedback/',
        customerviews.feedback_form,
        name='feedback_form'
    ),

    path(
        'contact/',
        customerviews.index,
        name='index'
    ),

    path(
        '',
        customerviews.Home,
        name='Home'
    ),

    path(
        'review/<int:food_id>/',
        customerviews.add_review,
        name='add_review'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )