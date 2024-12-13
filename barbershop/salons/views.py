from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Salon
from .serializers import SalonSerializer
from users.serializers import BarberSerializer  # Barber serializerini əlavə edin
from users.models import Barber  # Barber modelini əlavə edin


class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

    def get_queryset(self):
        queryset = Salon.objects.all()
        name = self.request.query_params.get('name', None)
        phone_number = self.request.query_params.get('phone_number', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if phone_number is not None:
            queryset = queryset.filter(phone_number=phone_number)

        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        salon_name = response.data.get('name')
        print(f"Yeni salon yaradıldı: {salon_name}")
        return response

    def update(self, request, *args, **kwargs):
        salon = self.get_object()
        response = super().update(request, *args, **kwargs)
        print(f"Salon yeniləndi: {salon.name} -> {response.data.get('name')}")
        return response

    @action(detail=True, methods=['get'])
    def barbers(self, request, pk=None):
        salon = self.get_object()
        barbers = salon.barbers.all()  # Salonun bütün bərbərlərini alın
        serializer = BarberSerializer(barbers, many=True)  # Barberlərin serializerini istifadə edin
        return Response(serializer.data)
