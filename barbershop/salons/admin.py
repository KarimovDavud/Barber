from django.contrib import admin
from .models import Salon
from salons.forms import SalonAdminForm
# Register your models here.

class SalonAdmin(admin.ModelAdmin):
    form = SalonAdminForm
    list_display = ['name', 'address', 'phone', 'description', 'tiktok_username', 'instagram_username']
    fields = ['name', 'address', 'phone', 'description', 'barbers', 'services', 'image', 'tiktok_username', 'instagram_username']

admin.site.register(Salon, SalonAdmin)
