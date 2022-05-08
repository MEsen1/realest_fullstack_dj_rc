from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginAPIView, RegistrationAPIView, LogoutAPIView, UserUpdateAPIView

router = routers.SimpleRouter()
router.register("list", UserUpdateAPIView)

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register_user"),
    path("login/", LoginAPIView.as_view(), name="login_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout_user"),
    # path("user/", UserUpdateAPIView.as_view(), name="user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
