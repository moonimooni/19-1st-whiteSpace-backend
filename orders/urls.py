from django.urls import path

from .cart_views import CartView

urlpatterns = [
    path('/cart', CartView.as_view())
]