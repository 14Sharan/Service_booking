from django.shortcuts import render,redirect
from accounts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.db.models import Q
from django.http import JsonResponse


def index(request):
    users = User.objects.all().count()
    return render(request,'admin/index.html',{"users":users,"head_title":"Dashboard"})


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user.is_superuser:
            login(request,user)
            return redirect('accounts:index')
        elif not user.is_superuser:
            login(request,user)
            return redirect('accounts:signup')
        return render(request,"registration/signin.html")
    return render(request,"registration/signin.html")

def LogOut(request):
    logout(request)
    return redirect("accounts:signup")


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

