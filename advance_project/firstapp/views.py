from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User



def HomeView(request):
    template_name = 'firstapp/home.html'
    return render(request,template_name)

def SignUpView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Used")
            return redirect('signup')
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username Already Used")
            return redirect('signup')
        else:
            user = User.objects.create_user(username = username,email = email  , password = password)
            user.save()
            send_mail('Signed In', f'You have Sign in {email}','rahulgirje8897@gmail.com',[email])
            messages.success(request, f'Account Create  {email}')
    template_name = 'firstapp/signup.html'
    return render(request,template_name)

def LoginView(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are Log in {u}')
            send_mail('Log In', f'You have logged in using{u}','rahulgirje8897@gmail.com',[email])
            return redirect('home')
        else:
            messages.error(request, 'Data not match')
    template_name = 'firstapp/login.html'
    return render(request,template_name)

def LogoutView(request):
    logout(request)
    return redirect('home')


def Changepassview(request):
    if request.method == 'POST':
        u=request.POST.get('uname')
        p=request.POST.get('password')
        np=request.POST.get('newpass')
        np1=request.POST.get('newpass1')
        email=request.POST.get('email')
        user=authenticate(username=u,password=p)
        if user and np==np1:
            usr=User.objects.get(username=u)
            npass=str(np1)
            usr.set_password(npass)
            usr.save()
            subject='Password Change'
            admin='rahulgirje8897@gmail.com'
            msj=f'Hello {usr} ,  password Successfully change, save your new password  services Link:-http://127.0.0.1:8000/auth/login/ '
            send_mail(subject,msj,admin,[email],fail_silently=True)
            logout(request)
            return redirect('login')
        messages.error(request,'Please Insert Correct Data')
    template_name='firstapp/change_password.html'
    return render(request,template_name)
