from rest_framework.routers import DefaultRouter

from radio.views import RadioViewSet

app_name = "radio"

router = DefaultRouter()
router.register("", RadioViewSet, basename="radio")

urlpatterns = router.urls
