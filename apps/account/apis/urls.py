from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterUserView, LogoutView, UserListView, UserDetailView

app_name = "account"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
