from django.db import models

class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    description = models.TextField()
    barbers = models.ManyToManyField('users.Barber', blank=True, related_name='salon_list')
    services = models.ManyToManyField('services.SalonServices', blank=True, related_name='salons_list')
    image = models.ImageField(upload_to='salon', blank=True, null=True)  # Allow blank and null
    tiktok_username = models.CharField(max_length=100, blank=True, null=True)
    instagram_username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128)


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
        return self.name
