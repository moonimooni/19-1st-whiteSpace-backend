from django.urls import path

from .views import ProductsView, ProductView
from .search_views import SearchView

urlpatterns = [
    path('/search', SearchView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
    path('', ProductsView.as_view())
]