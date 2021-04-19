from django.urls import path, re_path

from .views import ProductsView

urlpatterns = [
    re_path(r'^(?:page=(?P<page>\d+))?$', ProductsView.as_view())
]