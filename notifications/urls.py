from rest_framework.routers import DefaultRouter
from .views import NotificationModelViewSet


router = DefaultRouter()
router.register(r'notifications', NotificationModelViewSet)

urlpatterns = router.urls