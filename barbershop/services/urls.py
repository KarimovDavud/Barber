from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import *


# REST Framework router-i üçün
router = DefaultRouter()
router.register(r'salonservices', SalonServicesViewset)
router.register(r'barberservices', BarberServicesViewset)
router.register(r'pricecurency', PriceCurencyViewset)

app_name = 'services'

urlpatterns = [
    path('api/', include(router.urls)),  # API görünüşlər üçün
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)