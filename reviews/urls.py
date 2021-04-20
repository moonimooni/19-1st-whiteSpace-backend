from django.urls import path

from .views import ReviewView

urlpatterns = [
    path('/<int:product_id>/reviews', ReviewView.as_view())
]