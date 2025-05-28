from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = "administration"

router = DefaultRouter()
router.register("users", AdminUserViewSetViewSet, basename="users")

urlpatterns = [
    path("login/", AdminObtainTokenView.as_view(), name="token"),
]

urlpatterns += router.urls
