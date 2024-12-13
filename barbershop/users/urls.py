from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .views import *
from . import views


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'barber', BarberViewSet)
router.register(r'gender', GenderViewSet)
router.register(r'dayofweek', DayOfWeekViewSet)
router.register(r'workinghour', WorkingHourViewSet)
router.register(r'appointments', AppointmentViewSet)



urlpatterns = [
    path('api', include(router.urls)),
    path('', home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('salons/salon/<int:pk>/', views.salon_detail, name='salon_detail'),
    path('barber-detail/<int:pk>/', views.barber_detail, name='barber_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('login_register/', views.login_register, name='login_register'),
    path('register_barber/', views.register_barber, name='register_barber'),
    path('register_salon/', views.register_salon, name='register_salon'),
    path('register_choices', views.register_choices, name='register_choices'),
    path('available_slots/<str:selected_date>/', views.available_slots, name='available_slots'),
    path('book_appointment/<int:barber_id>/<str:selected_date>/<str:selected_time>/', views.book_appointment, name='book_appointment'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
