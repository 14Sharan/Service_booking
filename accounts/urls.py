from django.urls import path
from accounts.views import *
app_name='accounts'
urlpatterns = [
    path('admin-index/',index,name="index"),
    path('',LoginView,name="login"),
    path('Logout/',LogOut,name="logout"),
    path('validat-email/',ValidateEmail,name ="validate_email")
]
