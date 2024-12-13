from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from .models import SalonServices, BarberServices, PriceCurency
from .serializers import SalonServicesSerializer, BarberServicesSerializer, PriceCurencySerializer




class SalonServicesViewset(viewsets.ModelViewSet):
    queryset = SalonServices.objects.all()
    serializer_class = SalonServicesSerializer


class BarberServicesViewset(viewsets.ModelViewSet):
    queryset = BarberServices.objects.all()
    serializer_class = BarberServicesSerializer

class PriceCurencyViewset(viewsets.ModelViewSet):
    queryset = PriceCurency.objects.all()
    serializer_class = PriceCurencySerializer
