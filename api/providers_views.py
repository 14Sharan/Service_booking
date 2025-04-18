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



class ServiceProviderProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["Service Provider Profile"],
        operation_id="Get User Profile",
        operation_description="Retrieve the authenticated user's profile",
    )
    def get(self, request):
        serializer = UserSerializer(request.user,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateServiceProviderProfile(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=['Service Provider Profile'],
        operation_id = "UpdateServiceProviderProfile",
        operation_description = "UpdateServiceProviderProfile",
        manual_parameters = [
            openapi.Parameter('name',openapi.IN_FORM,type=openapi.TYPE_STRING),
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

        serializer = ServiceProviderSerializer(service_provider_profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        
        return Response({"message": "Profile update failed", "errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


class AddService(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Service'],
        operation_id="AddService",
        operation_description="Add a new service for a provider",
        request_body=ServiceSerializer
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = ServiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(service_provider=user)
            return Response({
                "message": "Service added successfully",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Validation failed",
            "errors": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

class ServicesList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Service'],
        operation_id="Services List",
        operation_description="List services of provider (optional: filter by service_type or service_name)",
        manual_parameters=[
            openapi.Parameter('service_type', openapi.IN_QUERY, description="Filter by service_type ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('service_name', openapi.IN_QUERY, description="Filter by service name", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        service_type = request.query_params.get('service_type')
        service_name = request.query_params.get('service_name')
        
        queryset = Service.objects.filter(service_provider=request.user)
        filters = Q()
        if service_type:
            filters |= Q(service_type=service_type)
        if service_name:
            filters |= Q(service_name__icontains=service_name)

        if filters:
            queryset = queryset.filter(filters)

        paginator = ServicePagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ServiceSerializer(paginated_queryset, many=True,context={'request': request})

        return paginator.get_paginated_response(serializer.data)
    

class ServiceUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Service'],
        operation_id="Services Update",
        operation_description="Update the service of provider",
        request_body=ServiceSerializer
    )
    def put(self, request, pk):
        
        service = get_object_or_404(Service, pk=pk, service_provider=request.user)
        serializer = ServiceSerializer(service, data=request.data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        tags=['Service'],
        operation_id="Services Delete",
        operation_description="Delete the service of provider",
        manual_parameters=[
        ]
    )

    def delete(self, request, pk):
        service = get_object_or_404(Service, pk=pk, service_provider=request.user)
        service.delete()
        return Response({"message": "Service deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ViewService(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Service'],
        operation_id="View Service",
        operation_description="Get details of a specific service by its ID",
        manual_parameters=[
        ]
    )
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk, service_provider=request.user)
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
