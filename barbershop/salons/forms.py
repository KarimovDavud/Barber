from django import forms
from salons.models import  Salon

class SalonAdminForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
