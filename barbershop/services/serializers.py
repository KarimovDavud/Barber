from rest_framework import serializers
from .models import SalonServices, BarberServices, PriceCurency

class SalonServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonServices
        fields = '__all__'

class BarberServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberServices
        fields = '__all__'

class PriceCurencySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCurency
        fields = '__all__'