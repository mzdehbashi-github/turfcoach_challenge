from rest_framework import routers

from pitch_health.views import v1


router = routers.SimpleRouter()
router.register(r'v1/pitch', v1.PitchViewSet)
urlpatterns = router.urls
