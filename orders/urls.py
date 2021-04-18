from django.urls import path

from .views import CartView

urlpatterns = [
    path('/cart/add', CartView.as_view())
]