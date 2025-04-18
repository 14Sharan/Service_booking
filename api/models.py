from django.db import models
from django.utils import timezone
import datetime
from accounts.models import User
from superuser.models import ServiceCategory
from accounts.constants import BOOKING_STATUS


class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.timestamp + datetime.timedelta(minutes=1)


class Service(models.Model):
    service_name = models.CharField(max_length=255, null=True, blank=True)
    service_type = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    service_image = models.FileField(upload_to='service_images/', null=True, blank=True)
    service_description = models.TextField(null=True, blank=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_provider")

    class Meta:
        managed = True
        db_table = "tbl_service"


class ServiceBooking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_booking")
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(choices=BOOKING_STATUS, default=1)
    service_date = models.DateTimeField(null=True, blank=True)
    service_time = models.TimeField(null=True, blank=True)
    service_address = models.TextField(null=True, blank=True)
    service_rating = models.IntegerField(null=True, blank=True)
    service_review = models.TextField(null=True, blank=True)
    class Meta:
        managed = True
        db_table = "tbl_service_booking"
