from django.urls import path

from .views import (
    LogIn,
    success,
    user_logout,
    SignUp
)

urlpatterns = [
    path("login/", LogIn.as_view(), name="login"),
    path("", success, name="success"),
    path("logout/", user_logout, name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
]
