from django.shortcuts import render, redirect
from accounts.models import *
from accounts.constants import *
from django.contrib.auth.decorators import login_required


@login_required
def UsersList(request):
    users = User.objects.filter(role_id =USER).order_by("-created_on")
    return render(request, "admin/users/users_list.html", {"users": users,"head_title":"users"})

@login_required
def ServiceProvidersList(request):
    users = User.objects.filter(role_id =SERVICE_PROVIDER).order_by("-created_on")
    return render(request, "admin/users/service_providers_list.html", {"users": users,"head_title":"service_providers"})


@login_required
def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.user_status = DELETED
    user.save()
    return redirect('superuser:all_users')

@login_required
def ServiceProviderProfile(request, id):
    if request.method  == "GET":
        user = User.objects.get(id=id)
        service_provider_info = ServiceProviderInfo.objects.get(user=user)
        return render(request, "admin/users/user-profile.html", {"user": user,"service_provider_info":service_provider_info})

"""
Activate User
"""
@login_required
def Activate_user(request,id):
    user=User.objects.get(id=id)
    user.user_status = ACTIVE
    user.save()
    return redirect('superuser:user_profile',id = id)

"""
In-activate User
"""
@login_required
def Inactive_user(request,id):
    user=User.objects.get(id=id)
    user.user_status = INACTIVE
    user.save()
    return redirect('superuser:user_profile',id = id)


