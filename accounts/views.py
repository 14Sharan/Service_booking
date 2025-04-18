from django.shortcuts import render,redirect
from accounts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages


def index(request):
    users = User.objects.all().count()
    return render(request,'admin/index.html',{"users":users,"head_title":"Dashboard"})


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('accounts:index')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('accounts:login')
    return render(request,"registration/login.html")

def LogOut(request):
    logout(request)
    return render(request,"registration/login.html")


"""
Validate email for existing email
"""
def ValidateEmail(request):
    data = {"is_exist":"false"}
    user = User.objects.filter(email = request.GET.get('email'))
    if user:
        data['is_exist']="true"
    else:
        data['is_exist']="false"
    return JsonResponse(data)

