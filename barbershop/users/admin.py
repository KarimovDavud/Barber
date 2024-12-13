from django.contrib import admin
from .models import Barber, Profile, WorkingHour, Appointment, Gender, DayOfWeek


class BarberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'address', 'gender', 'birth_date')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('gender', 'salons', 'services')
    list_per_page = 20


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'name', 'phone', 'birth_date', 'gender', 'address')
    search_fields = ('name', 'phone')
    list_filter = ('gender', 'salon')
    list_per_page = 20

class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ('barber', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'start_time', 'end_time')
    search_fields = ('barber__first_name', 'barber__last_name')
    list_per_page = 20

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('barber', 'user', 'appointment_time')
    list_filter = ('barber', 'appointment_time')
    search_fields = ('user__username', 'barber__first_name', 'barber__last_name')
    list_per_page = 20


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20


class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20


# Register models
admin.site.register(Barber, BarberAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(WorkingHour, WorkingHourAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(DayOfWeek, DayOfWeekAdmin)
