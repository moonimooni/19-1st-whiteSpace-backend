from django.urls import path

from .views import SignUpView, SignInView, CheckEmailView, OrderUserInfoView

urlpatterns = [
    path('/info', OrderUserInfoView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/check-email', CheckEmailView.as_view())                                   
] 
