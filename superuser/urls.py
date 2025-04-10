from django.urls import path,include
from .views import *
app_name='superuser'
urlpatterns = [
    path('users-list/',UsersList,name='users_list'),
    path('service-providers-list/',ServiceProvidersList,name='service_providers_list'),
    path('delete-user/<int:id>',DeleteUser,name='delete_user'),
    path('service-provider-profile/<int:id>',ServiceProviderProfile,name='service_provider_profile'),
    path('activate-user/<int:id>',Activate_user,name='activate_user'),
    path('inactive-user/<int:id>',Inactive_user,name='inactive_user'),
   
] 