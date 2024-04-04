from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView

app_name = 'users'

urlpatterns = [
    path('user/register/', UserRegistrationAPIView.as_view(), name="register"),
    path('user/login/', UserLoginAPIView.as_view(), name="login"),
]
