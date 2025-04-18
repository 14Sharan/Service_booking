from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.constants import *
from datetime import datetime
class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    role_id = models.PositiveIntegerField(default=1, choices=USER_ROLE, null=True, blank=True)
    user_status = models.PositiveIntegerField(default=ACTIVE, choices=USER_STATUS, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "tb_user"
        
    def __str__(self):
        return self.username or self.mobile_no or str(self.id)


class ServiceProviderInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="service_provider_info")
    verification_status = models.PositiveIntegerField(default=1, choices=VERIFICATION_STATUS)
    verified_on = models.DateTimeField(default=datetime.now)
    rejection_reason = models.TextField(null=True, blank=True)
    break_status = models.PositiveIntegerField(default=False)
    document_type = models.PositiveIntegerField(choices=DOCUMENT_TYPES)  # Remove blank=True
    document_file = models.FileField(upload_to='verification_documents') 
    uploaded_on = models.DateTimeField(auto_now_add=True)
 # Remove blank=True
    
    class Meta:
        managed = True
        db_table = "tb_service_provider_info"

