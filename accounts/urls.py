from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserRetrieveView,
    UserUpdateView,
    UserDeleteView,
    ChangePasswordView
)

urlpatterns = [
    # Register
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Current logged-in user
    path("me/", UserRetrieveView.as_view(), name="user-detail"),
    path("me/update/", UserUpdateView.as_view(), name="user-update"),
    path("me/delete/", UserDeleteView.as_view(), name="user-delete"),
     path("me/change-password/", ChangePasswordView.as_view(), name="change-password"),
]