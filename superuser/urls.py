from django.urls import path,include
from .views import *
app_name='superuser'
urlpatterns = [
    path('users-list/',UsersList,name='users_list'),
    path('service-providers-list/',ServiceProvidersList,name='service_providers_list'),
    path('user-profile/<int:id>',UserProfile,name='user_profile'),
    path('service-provider-profile/<int:id>',ServiceProviderProfile,name='service_provider_profile'),
    path('admin-profile/<int:id>',AdminProfile,name='admin_profile'),
    path('delete-user/<int:id>',DeleteUser,name='delete_user'),
    path('verfiy-service-provider-profile/<int:id>',VerfiyServiceProviderProfile,name='verfiy_service_provider_profile'),
    path('reject-service-provider-profile/<int:id>',RejectServiceProviderProfile,name='reject_service_provider_profile'),
    #Servicej
    path('add-category/',AddCategory,name='add_category'),
    path('delete-category/<int:id>',DeleteCategory,name='delete_category'),
    path('edit-category/',EditCategory,name='edit_category'),
    path('user-graph/',UserGraph,name='user_graph'),

] 