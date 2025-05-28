from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from ekilauth.authentification.views import EkilAuthViewSet
from ekilauth.authentification.views import ObtainTokenView

router = DefaultRouter()
router.register("", EkilAuthViewSet, basename="users")

urlpatterns = [
    path("login/", ObtainTokenView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
