from django.urls import path

from .cart_views  import CartView
from .order_views import OrderFromCartView

urlpatterns = [
    path('/order', OrderFromCartView.as_view()),
    path('/<int:item_id>', CartView.as_view()),
    path('', CartView.as_view())
]