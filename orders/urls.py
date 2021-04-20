from django.urls import path

from .cart_views import CartView

urlpatterns = [
    path('/<int:item_id>', CartView.as_view()),
    path('', CartView.as_view())
]