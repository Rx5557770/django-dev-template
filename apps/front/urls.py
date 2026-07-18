from django.urls import path
from . import views

app_name = "front"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
]
