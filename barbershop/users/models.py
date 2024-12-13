from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from salons.models import Salon
from django.utils import timezone


class Gender(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class DayOfWeek(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Barber(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='media/barber', blank=True)
    description = models.TextField()
    services = models.ManyToManyField('services.BarberServices', related_name='barbers_list', blank=True)
    salons = models.ManyToManyField('salons.Salon', blank=True, related_name='barbers_in_salon')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    birth_date = models.DateField(null=True, blank=True)
    tiktok_username = models.CharField(max_length=100, blank=True, null=True)
    instagram_username = models.CharField(max_length=100, blank=True, null=True)
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=128)
    workinghours = models.ManyToManyField('WorkingHour', related_name='barbers', blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    @property
    def tiktok_link(self):
        if self.tiktok_username:
            return f"https://www.tiktok.com/@{self.tiktok_username}"
        return None

    @property
    def instagram_link(self):
        if self.instagram_username:
            return f"https://www.instagram.com/{self.instagram_username}"
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(m2m_changed, sender=Barber.salons.through)
def update_address(sender, instance, action, **kwargs):
    """
    Barber modelində salons sahəsi dəyişdirildikdə address sahəsini yeniləyir.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.salons.exists():
            instance.address = ', '.join(salon.address for salon in instance.salons.all())
        else:
            instance.address = ''  # Heç bir salon yoxdursa, address boş qoyulur.
        instance.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=16)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tiktok_username = models.CharField(max_length=50, null=True, blank=True)
    instagram_username = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='media/barber', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username



class WorkingHour(models.Model):
    barber = models.ForeignKey(Barber, related_name='working_hours', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.barber} - {self.start_time} to {self.end_time}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

class Appointment(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    appointment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.barber.first_name} {self.barber.last_name} - {self.appointment_time}"
