from django.shortcuts import render, redirect
from accounts.models import *
from accounts.constants import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from superuser.models import ServiceCategory
from api.models import PhoneOTP
from django.http import JsonResponse
from superuser.decorator import admin_only
import calendar
@login_required
def UsersList(request):
    users = User.objects.filter(role_id =USER,user_status=ACTIVE).order_by("-created_on")
    return render(request, "users/end_user/users-list.html", {"users": users,"head_title":"Users"})

@login_required
def ServiceProvidersList(request):
    users = User.objects.filter(role_id =SERVICE_PROVIDER,user_status=ACTIVE).order_by("-created_on")
    profile_status = ServiceProviderInfo.objects.filter(user__in=users)
    return render(request, "users/service_provider/users-list.html", {"users": users,"head_title":"Service Providers","profile_status":profile_status})


@login_required
def UserProfile(request, id):
    if request.method  == "GET":
        user = User.objects.get(id=id)
        return render(request, "users/end_user/profile.html", {"user": user,"head_title":"Users"})
    
@login_required
def AdminProfile(request, id): 
    if request.method  == "GET":
        user = User.objects.get(id=id)
        return render(request, "admin/admin-profile.html", {"user": user})   
    if request.method == "POST":
        user = User.objects.get(id=id)
        if request.POST.get("full_name"):
            user.full_name = request.POST.get("full_name")
        if request.POST.get("address"):
            user.address = request.POST.get("address")
        if request.POST.get("city"):
            user.city = request.POST.get("city")
        if request.POST.get("country"):
            user.country = request.POST.get("country")
        if request.POST.get("postal_code"):
            user.postal_code = request.POST.get("postal_code")
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("superuser:user_profile", id=id)


@login_required
def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.user_status = DELETED
    user.save()
    PhoneOTP.objects.get(phone_number=user.mobile_no).delete()
    if user.role_id == SERVICE_PROVIDER:
        return redirect('superuser:service_providers_list')
    else:
        return redirect('superuser:users_list')
@login_required
def ServiceProviderProfile(request, id):
    if request.method  == "GET":
        user = User.objects.get(id=id)
        service_provider_info = ServiceProviderInfo.objects.get(user=user)
        verification_status=service_provider_info.verification_status
        return render(request, "users/service_provider/profile.html", {"user": user,"service_provider_info":service_provider_info,"verification_status":verification_status,"head_title":"service_provider_profile","head_title":"Service Providers"})

@login_required
def VerfiyServiceProviderProfile(request,id):
    user=User.objects.get(id=id)
    profile_status=ServiceProviderInfo.objects.get(user=user)
    if profile_status.verification_status == VERIFIED:
        messages.error(request,"Service provider's profile already verified.")
        return redirect('superuser:service_provider_profile',id = id)
    profile_status.verification_status=VERIFIED
    profile_status.save()
    messages.success(request,"Service provider's profile verified successfully.")
    return redirect('superuser:service_provider_profile',id = id)


@login_required
def RejectServiceProviderProfile(request,id):
    user=User.objects.get(id=id)
    profile_status=ServiceProviderInfo.objects.get(user=user)

    if profile_status.verification_status == REJECTED:
        messages.error(request,"Service provider's profile already rejected.")
        return redirect('superuser:service_provider_profile',id = id)
    profile_status.verification_status=REJECTED
    profile_status.save()
    messages.success(request,"Service provider's profile rejected successfully.")
    return redirect('superuser:service_provider_profile',id = id)


@login_required
def AddCategory(request):
    if request.method == "GET":
        categories = ServiceCategory.objects.all()
        if request.GET.get('category_title'):
            categories = categories.filter(category_title__icontains = request.GET.get('category_title').strip())
        return render(request, "admin/category/categoty.html", {"categories": categories,"head_title":"Add Category"})
    if request.method == "POST":
        if not request.POST.get("category_name"):
            messages.error(request, "Category name is required.")
            return redirect("superuser:add_category")
        if ServiceCategory.objects.filter(category_title=request.POST.get("category_name")).exists():
            messages.error(request, "Category already exists.")
            return redirect("superuser:add_category")
        category_name = request.POST.get("category_name")
        ServiceCategory.objects.create(category_title=category_name,created_by=request.user)
        messages.success(request, "Category added successfully.")
        return redirect("superuser:add_category")
    

@login_required
def EditCategory(request):
    if request.method == "GET":
        id = request.POST.get("id")
        category = ServiceCategory.objects.get(id=id)
        return render(request, "admin/category/edit-category.html", {"category": category,"head_title":"Edit Category"})
    if request.method == "POST":
        if not request.POST.get("category_name"):
            messages.error(request, "Category name is required.")
            return redirect("superuser:add_category")
        if ServiceCategory.objects.filter(category_title=request.POST.get("category_name")).exists():
            messages.error(request, "Category already exists.")
            return redirect("superuser:add_category")
        id = request.POST.get("id")
        category = ServiceCategory.objects.get(id=id)
        category.category_title = request.POST.get("category_name")
        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect("superuser:add_category")
    
@login_required
def DeleteCategory(request, id):
    category = ServiceCategory.objects.get(id=id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("superuser:add_category")


@admin_only
def UserGraph(request):
    selected_year = str(request.GET.get('year')) if request.GET.get('year') else str(datetime.now().year)
    selected_month = str(request.GET.get('month')) if request.GET.get('month') else str(datetime.now().month)
    user = User.objects.filter(created_on__year=selected_year,created_on__month=selected_month,role_id=USER).count()
    service_provider = User.objects.filter(created_on__year=selected_year,created_on__month=selected_month,role_id=SERVICE_PROVIDER).count()

    try:
        service_provider_percent = round((service_provider/(service_provider+user))*100,1)
    except:
        service_provider_percent = 0
    try:
        user_percent = round((user/(service_provider+user))*100,1)
    except:
        user_percent = 0    
   

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': '', 'align': 'left'},
        'legend': {'align': 'right', 'verticalAlign': 'top'},
        'colors': ["#ff0000 ","#0000FF","#008000"],
        'series':[{
            'name': 'Users',
            'colorByPoint': True,
            'data': [
                {
                    'name': 'Service Providers',
                    'y':service_provider,
                    'x':service_provider_percent
                }, 
                {
                    'name': 'User',
                    'y':user,
                    'x':user_percent
                },
              
            ]
        }],
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format':'{point.name}: {point.x} %'
                }
            }
        },
    }
    return JsonResponse({"chart":chart,"selected_year":selected_year,"month_name":calendar.month_name[int(selected_month)],"selected_month":selected_month},safe=False)
