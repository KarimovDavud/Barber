from django.contrib import admin
from .models import SalonServices, BarberServices, PriceCurency

# Register your models here.

admin.site.register(SalonServices)
admin.site.register(BarberServices)
admin.site.register(PriceCurency)