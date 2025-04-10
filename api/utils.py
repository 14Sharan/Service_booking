from django.http import JsonResponse
from .models import PhoneOTP
import random
def generate_otp():
    return str(random.randint(100000, 999999))
def send_otp_view(mobile_no):
    otp = generate_otp()
    PhoneOTP.objects.update_or_create(phone_number=mobile_no, defaults={'otp': otp, 'is_verified': False})
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f'Your OTP is {otp}',
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number
    # )
    message = f'Your OTP is {otp}'
    return message

   
