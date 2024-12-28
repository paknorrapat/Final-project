from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from datetime import datetime
from .models import User,Profile

# Create your views here.
def firstpage(request):
    return render(request,"firstpage.html")

def calculate_age(birth_date):
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def showprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    age = calculate_age(user.profile.birthDate)  # คำนวณอายุ
    return render(request, "sparky/profile.html", {'user': user, 'age': age})  # ส่งค่าอายุไปยังเทมเพลต


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # ใช้ cleaned_data เพื่อความปลอดภัย
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request,user)
                if user.is_staff:
                    # Redirect ไปหน้า staff
                    return redirect('staff-home')
                elif user.is_manager:
                    # Redirect ไปหน้า manager
                    return redirect('manager-home')
                elif user.is_dentist:
                    # Redirect ไปหน้า dentist
                    return redirect('dentist-home')
                else:
                    # Redirect ไปหน้า member
                    return redirect('member-home')
            else:
                messages.error(request,'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = LoginForm()
    return render(request,'registration/login.html',{'form':form})

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('firstpage')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('profile-form',user_id=user.id)   
        else:
            messages.error(request, 'ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบข้อมูลที่กรอก')
    else:
        form = RegisterForm()

    return render(request,'registration/register.html',{'form':form})

def profile(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
        
    else:
        profile_form = ProfileForm()
    
    return render(request,'registration/profile_form.html',{'profile_form':profile_form})


def updateprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        # อัปเดตฟิลด์ของผู้ใช้
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.title = request.POST.get('title')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        
        # อัปเดตฟิลด์ของโปรไฟล์
        profile.idCard = request.POST.get('idCard')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.gender = request.POST.get('gender')
        profile.weight = request.POST.get('weight')
        profile.height = request.POST.get('height')
        profile.bloodType = request.POST.get('bloodType')
        profile.ud = request.POST.get('ud')
        profile.allergic = request.POST.get('allergic')
        profile.birthDate = request.POST.get('birthDate')
        
        # อัปเดตรูปภาพโปรไฟล์ถ้ามีการอัปโหลด
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        # บันทึกการเปลี่ยนแปลงในผู้ใช้และโปรไฟล์
        try:
            user.save()
            profile.save()
            messages.success(request, 'อัปเดตโปรไฟล์สำเร็จแล้ว')
            return redirect('profile', user_id=user.id)
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาดในการอัปเดตโปรไฟล์ของคุณ: {e}")
    
    return render(request, 'sparky/update_profile.html', {'user': user, 'profile': profile})