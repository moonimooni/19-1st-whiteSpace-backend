from django.urls import path

from .cart_views import CartView

urlpatterns = [
    path('', CartView.as_view())
]