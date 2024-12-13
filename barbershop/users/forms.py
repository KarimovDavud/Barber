from django import forms
from salons.models import *
from users.models import *




class SalonForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Salon
        fields = [
            'name', 'address', 'phone', 'description', 
            'barbers', 'services', 'image', 
            'tiktok_username', 'instagram_username', 'password'
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'barbers': forms.CheckboxSelectMultiple(),  # Use checkboxes for many-to-many field
            'services': forms.CheckboxSelectMultiple(),  # Use checkboxes for many-to-many field
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data



class BarberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Barber
        fields = [
            'first_name', 'last_name', 'phone_number', 'email', 'address', 
            'description', 'services', 'image', 'tiktok_username', 
            'instagram_username', 'gender', 'birth_date', 'day_of_week'
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = '__all__' 

    phone = forms.CharField(max_length=15)
    birth_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data

class BarberRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Barber
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'description', 'services', 'image', 'tiktok_username', 'instagram_username',  'gender', 'day_of_week']  
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
        }
    birth_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('��ifrələr uyğun gəlmir.')

        return cleaned_data


class SalonRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Şifrə')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Şifrəni Təkrarla')

    class Meta:
        model = Salon
        fields = [
            'name', 'address', 'phone', 'description', 
            'barbers', 'services', 'image', 
            'tiktok_username', 'instagram_username'
        ]  # Explicitly list the fields you want to include

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data