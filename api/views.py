from rest_framework.views import APIView 
from accounts.models import *
from api.serializer import *
from rest_framework import  permissions,status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.utils import send_otp_view
from api.models import PhoneOTP
from rest_framework_simplejwt.tokens import RefreshToken

class SendOtp(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['User Authentication'],
        operation_id = "SendOtp",
        operation_description = "SendOtp",
        manual_parameters = [
            openapi.Parameter('mobile_no',openapi.IN_FORM,type=openapi.TYPE_STRING,required=True,description="Mobile number"),
        ]
    )
    def post(self,request,*args,**kwargs):
        mobile_no = request.data.get('mobile_no')
        if not mobile_no:
            return Response({"message":"Mobile number is required","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile_no=mobile_no,user_status=ACTIVE).exists():
            return Response({"message":"Mobile number already exists","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        User.objects.create(mobile_no=mobile_no,role_id=USER)
        otp=send_otp_view(mobile_no)
        return Response({"otp":otp,"message":"An OTP has sent to your mobile number","status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class ResendOTP(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['User Authentication'],
        operation_id = "ResendOTP",
        operation_description = "ResendOTP",
        manual_parameters = [
            openapi.Parameter('mobile_no',openapi.IN_FORM,type=openapi.TYPE_STRING,required=True,description="Mobile number"),
        ]
    )
    def post(self,request,*args,**kwargs):
        mobile_no = request.data.get('mobile_no')
        if not mobile_no:
            return Response({"message":"Mobile number is required","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(mobile_no=mobile_no).exists():
            return Response({"message":"Mobile number does not exist","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        try:
            phone_otp = PhoneOTP.objects.get(phone_number=mobile_no)
        except PhoneOTP.DoesNotExist:
            return Response({"message":"OTP does not exist","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if phone_otp.is_expired():
            phone_otp.delete()
            otp = send_otp_view(mobile_no)
            return Response({"otp":otp,"message":"An OTP has sent to your mobile number","status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        else:
            otp = send_otp_view(mobile_no)
            return Response({"otp":otp,"message":"An OTP has sent to your mobile number","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class VerifyOtp(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['User Authentication'],
        operation_id = "VerifyOtp",
        operation_description = "VerifyOtp",
        manual_parameters = [
            openapi.Parameter('mobile_no',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('otp',openapi.IN_FORM,type=openapi.TYPE_STRING),
        ]
    )
    def post(self,request,*args,**kwargs):
        phone = request.data.get('mobile_no')
        otp = request.data.get('otp')
        try:
            phone_otp = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            return Response({'error': 'Wrong OTP'}, status=status.HTTP_404_NOT_FOUND)
        if phone_otp.is_expired():
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        if phone_otp.otp == otp:
            phone_otp.is_verified = True
            phone_otp.save()    
            username = f"user_{phone}"
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message":"OTP verified successfully",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            })
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    

class ServiceproviderSignup(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['Service Provider Authentication'],
        operation_id = "ServiceproviderSignup",
        operation_description = "ServiceproviderSignup",
            manual_parameters = [
                openapi.Parameter('name',openapi.IN_FORM,type=openapi.TYPE_STRING),
                openapi.Parameter('email',openapi.IN_FORM,type=openapi.TYPE_STRING),
                openapi.Parameter('mobile_no',openapi.IN_FORM,type=openapi.TYPE_STRING),
                openapi.Parameter('document_type',openapi.IN_FORM,type=openapi.TYPE_INTEGER),
                openapi.Parameter('document_file',openapi.IN_FORM,type=openapi.TYPE_FILE),
                openapi.Parameter('password',openapi.IN_FORM,type=openapi.TYPE_STRING),
            ]
    )
    def post(self,request):
        name= request.data.get('name')
        email= request.data.get('email')
        mobile_no= request.data.get('mobile_no')
        password= request.data.get('password')
        document_type = request.data.get('document_type')
        document_file = request.FILES.get('document_file')
        if not name or not email or not mobile_no or not password or not document_file or not document_type:
            return Response({"message":"All fields are required","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"message":"Email already exists","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile_no=mobile_no).exists():
            return Response({"message":"Mobile number already exists","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=email,full_name=name,email=email,mobile_no=mobile_no,password=password,role_id=SERVICE_PROVIDER)
        user.set_password(password)
        user.save()
        ServiceProviderInfo.objects.create(user=user,document_type=document_type,document_file=document_file)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message":"Your registration is successfully done.Please wait for admin approval",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
            }
        },status=status.HTTP_200_OK)
    
class ServiceproviderLogin(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['Service Provider Authentication'],
        operation_id = "ServiceproviderLogin",
        operation_description = "ServiceproviderLogin",
        manual_parameters = [
            openapi.Parameter('email',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('password',openapi.IN_FORM,type=openapi.TYPE_STRING),
        ]
    )
    def post(self,request):
        email= request.data.get('email')
        password= request.data.get('password')
        if not email or not password:
            return Response({"messages":"All fields are required","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            provider = ServiceProviderInfo.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"messages":"User does not exist","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if provider.verification_status == PENDING:
            return Response({"messages":"Your Profile is not verified.Please wait for admin approval","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if provider.verification_status == REJECTED:
            return Response({"messages":"Your Profile is rejected by the admin","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({"messages":"Invalid password","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message":"Login Successfully",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
            }
        },status=status.HTTP_200_OK)