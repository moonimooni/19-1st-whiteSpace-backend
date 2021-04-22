from django.urls import path

from .views import ReviewView, ReviewAuthView

urlpatterns = [
    path('/<int:product_id>/reviews/auth', ReviewAuthView.as_view()),
    path('/<int:product_id>/reviews', ReviewView.as_view())
]