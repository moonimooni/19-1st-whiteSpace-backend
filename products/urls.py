from django.urls import path

from .views import ProductsView, ProductView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('', ProductsView.as_view())
]