from rest_framework.views import APIView 
from accounts.models import *
from api.serializer import *
from rest_framework import  permissions,status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.serializer import ServiceProviderSerializer
from django.db.models import Q
from api.utils import ServicePagination   
from django.shortcuts import get_object_or_404
from api.models import ServiceBooking

class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_id="Get User Profile",
        operation_description="Retrieve the authenticated user's profile",
    )
    def get(self, request):
        serializer = ServiceProviderSerializer(request.user,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['User Profile'],
        operation_id = "Update User Profile",
        operation_description = "Update User Profile",
        manual_parameters = [
            openapi.Parameter('full_name',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('address',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('city',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('state',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('country',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('postal_code',openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter('profile_pic',openapi.IN_FORM,type=openapi.TYPE_FILE),
        ]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated", "status": status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            service_provider_profile = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response({"message": "Service provider profile does not exist", "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        files = request.FILES
        if 'profile_pic' in files:
            data['profile_pic'] = files['profile_pic']

        serializer = UserSerializer(service_provider_profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        
        return Response({"message": "Profile update failed", "errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)



class BookService(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Book Service"],
        operation_id="Book Service",
        operation_description="Book a service for the authenticated user",
        manual_parameters=[
            openapi.Parameter('service_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER),
        ]
    )
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated", "status": status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)

        service_id = request.data.get('service_id')


        try:
            service = get_object_or_404(Service, id=service_id)
        except Service.DoesNotExist:
            return Response({"message": "Service does not exist", "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)

        booking = ServiceBooking.objects.create(
            customer=user,
            service=service,
        )

        return Response({"message": "Service booked successfully", "booking_id": booking.id, "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)