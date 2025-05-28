from rest_framework.routers import DefaultRouter

from radio.radio_menu.views import RadioMenuViewSet

app_name = "radio-menu"

router = DefaultRouter()
router.register("", RadioMenuViewSet, basename="radio")

urlpatterns = router.urls
