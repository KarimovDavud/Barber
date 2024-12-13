from django.db import models

class PriceCurency(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Bərbərin və salonun göstərdiyi xidmətlərin dataları.
class SalonServices(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default="Ödənişsiz")
    price_curency = models.ForeignKey(PriceCurency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class BarberServices(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_curency = models.ForeignKey(PriceCurency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
