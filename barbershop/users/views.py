from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib import messages
from salons.models import Salon
from services.models import *
from .serializers import *
from users.models import *
from users.forms import *
from .models import *


# API üçün ViewSet-lər
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BarberViewSet(viewsets.ModelViewSet):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class DayOfWeekViewSet(viewsets.ModelViewSet):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer

class WorkingHourViewSet(viewsets.ModelViewSet):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(barber=self.request.user.barber)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer




def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Burada token yaradılması və ya saxlanılması yoxdur

            return redirect('home')  # Uğurlu girişdən sonra ana səhifəyə yönləndirin
        else:
            messages.error(request, 'Yanlış istifadəçi adı və ya şifrə.')

    return render(request, 'users/login_user.html')


def register_salon(request):
    if request.method == 'POST':
        form = SalonRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            services = form.cleaned_data.get('services', [])
            barbers = form.cleaned_data.get('barbers', None)
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            password = form.cleaned_data['password']
            tiktok_username = form.cleaned_data['tiktok_username']
            instagram_username = form.cleaned_data['instagram_username']

            # Salon adının təkrar olmadığını yoxla
            if Salon.objects.filter(name=name).exists():
                messages.error(request, 'Bu salon adı artıq mövcuddur.')
                return render(request, 'users/register_salon.html', {'form': form})

            # Yeni kullanıcı oluştur
            user = User.objects.create_user(username=name, password=password)
            user.save()

            # Yeni salon obyektini yarat
            salon = Salon(
                name=name,
                address=address,
                phone=phone,
                password=make_password(password),
                tiktok_username=tiktok_username,
                instagram_username=instagram_username,
                image=image,
                description=description,
              
            )
            if barbers:
                salon.barbers.set(barbers)
            salon.save()

            # Salon xidmətlərini əlavə et
            for service in services:
                services_obj = SalonServices.objects.get(id=service.id)
                salon.services.add(services_obj)

            # Barber əlavə et, əgər seçilibsə
            if barbers:
                barber_objects = Barber.objects.filter(id__in=barbers)
                for barber in barber_objects:
                    salon.barbers.add(barber)

            # Profil yarat
            Profile.objects.create(
                user=user,  # Yeni oluşturulan kullanıcı nesnesi
                salon=salon,
                address=address,
                phone=phone,
                tiktok_username=tiktok_username,
                instagram_username=instagram_username,
                image=image,
                description=description,
            )

            # Oturum açma
            login(request, user)

            messages.success(request, 'Qeydiyyat uğurla tamamlandı.')
            return redirect('home')
        else:
            messages.error(request, 'Formda səhvlər var, zəhmət olmasa onları düzəldin.')
    else:
        form = SalonRegisterForm()

    return render(request, 'salons/register_salon.html', {'form': form})
def register_barber(request):
    if request.method == 'POST':
        form = BarberRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            # Check for existing email
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Bu e-posta adresi zaten kullanılıyor.')
                return redirect('register_barber')

            # Create User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data['password']
            )

            # Create Profile
            salon = Salon.objects.first()
            Profile.objects.create(
                user=user,
                name=form.cleaned_data['first_name'],
                phone=form.cleaned_data['phone_number'],
                salon=salon,
            )

            # Create Barber
            barber = Barber.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                email=email,
                address=form.cleaned_data['address'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                tiktok_username=form.cleaned_data.get('tiktok_username'),
                instagram_username=form.cleaned_data.get('instagram_username')
            )
            barber.salons.set([salon])  # Many-to-many relationship

            # Add Barber Services
            services_barber = form.cleaned_data['services']
            barber.services.add(*services_barber)

            messages.success(request, 'Qeydiyyat uğurla tamamlandı.')
            return redirect('home')
        else:
            # Handle form errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, f"General error: {error}")
                    else:
                        messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = BarberRegisterForm()

    services = BarberServices.objects.all()
    return render(request, 'users/register_barber.html', {
        'form': form,
        'services': services,
    })


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # İstifadəçi adı yoxlanması
        if not username:
            messages.error(request, 'İstifadəçi adı daxil edilməlidir.')
            return render(request, 'users/register_user.html')
        
        # E-mail yoxlanması
        if not email:
            messages.error(request, 'E-mail daxil edilməlidir.')
            return render(request, 'users/register_user.html')
        
        # Şifrələrin uyğunluğunu yoxlama
        if password != confirm_password:
            messages.error(request, 'Şifrələr uyğun deyil.')
            return render(request, 'users/register_user.html')

        # İstifadəçi adı artıq mövcuddur mu?
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu istifadəçi adı artıq mövcuddur.')
            return render(request, 'users/register_user.html')

        # İstifadəçini yarat
        user = User(username=username, email=email)
        user.set_password(password)  # Şifrəni burada təyin edirik
        user.first_name = first_name  # Adı burada təyin edirik
        user.last_name = last_name  # Soyadı burada təyin edirik
        user.save()  # İstifadəçini bazaya əlavə edirik
        
        # Profili yarat
        profile = Profile.objects.create(
            user=user,  # Burada 'user' obyektini veririk
            phone=phone, 
            gender=gender, 
            birth_date=birth_date
        )

        messages.success(request, 'Qeydiyyat uğurla tamamlandı.')
        return redirect('home')
    
    return render(request, 'users/register_user.html')


# Profilin redaktə olunması
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz uğurla yeniləndi.')
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'users/edit_profile.html', {'form': form})

# Profilin silinməsi
@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()  # İstifadəçini də silmək üçün
        messages.success(request, 'Profil və istifadəçi uğurla silindi.')
        return redirect('home')
    
    return render(request, 'users/delete_profile.html', {'profile': profile})


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'users/user_profile.html', context)

def login_register(request):
    return render(request, 'users/login_register.html')



@login_required(login_url='login_register')
def home(request):
    salons = Salon.objects.all()
    barbers = Barber.objects.all()

    return render(request, 'users/home.html', {
        'salons': salons,
        'users': barbers,
    })

@login_required
def salon_detail(request, pk):
    salon = get_object_or_404(Salon, pk=pk)
    services = salon.services.all()
    barbers = Barber.objects.filter(salons=salon)  
    return render(request, 'salons/salon_detail.html', {
        'salon': salon,
        'services': services,
        'barbers': barbers,
    })


@login_required
def barber_detail(request, pk):
    barber = get_object_or_404(Barber, pk=pk)
    services = barber.services.all()
    salons = barber.salons.all()  # `.all()` əlavə edin
    workinghours = barber.working_hours.all() 
    return render(request, 'users/barber_detail.html', {
        'barber': barber,
        'services': services,
        'salons': salons,
        'workinghours': workinghours,
    })


def login_register(request):
    return render(request, 'users/login_register.html')  

def register_choices(request):
    return render(request, 'users/register_choices.html')




def available_slots(request, selected_date):
    # Seçilen tarih için haftanın günü
    selected_day_of_week = selected_date.weekday()  # 0: Pazartesi, 6: Pazar

    # Berberin çalışma saatlerini alıyoruz
    working_hours = WorkingHour.objects.filter(day_of_week=selected_day_of_week)
    
    available_slots = []
    for hour in working_hours:
        available_slots.append({
            'barber': hour.barber,
            'start_time': hour.start_time,
            'end_time': hour.end_time,
        })

    return render(request, 'available_slots.html', {'available_slots': available_slots, 'selected_date': selected_date})

def book_appointment(request, barber_id, selected_date, selected_time):
    barber = Barber.objects.get(id=barber_id)
    
    # Seçilen saat çalışma saatleri içinde mi?
    selected_datetime = datetime.combine(selected_date, selected_time)
    working_hour = WorkingHour.objects.filter(
        barber=barber,
        day_of_week=selected_date.weekday(),
        start_time__lte=selected_time,
        end_time__gte=selected_time
    ).first()

    if not working_hour:
        return HttpResponse("Seçtiğiniz saat, berberin çalışma saatleri içinde değil.", status=400)

    # Randevuyu oluşturuyoruz
    appointment = Appointment.objects.create(
        barber=barber,
        user=request.user,  # Kullanıcı bilgisi
        start_time=selected_datetime,
        end_time=selected_datetime + timedelta(hours=1),  # 1 saatlik randevu
    )

    return redirect('appointment_success')  # Başarı sayfasına yönlendiriyoruz


