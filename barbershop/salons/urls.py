from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .views import SalonViewSet


router = DefaultRouter()
router.register('salon', SalonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
