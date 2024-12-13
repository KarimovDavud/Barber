from rest_framework import  serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    barber = BarberSerializer()
    class Meta:
        model = Appointment
        fields = '__all__'