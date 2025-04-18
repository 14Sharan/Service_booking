from accounts.models import *
from rest_framework import serializers 
from api.models import Service

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['full_name', 'address', 'city', 'state', 'country', 'postal_code', 'profile_pic','latitude','longitude']
    def get_service_image(self, obj):
        request = self.context.get('request')
        if obj.profile_pic and hasattr(obj.profile_pic, 'url'):
            return request.build_absolute_uri(obj.profile_pic.url)
        return None
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class ServiceProviderstausSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderInfo
        fields = [
            'verified_on',
            'break_status',
        ]
class ServiceProviderSerializer(serializers.ModelSerializer):
    service_provider_info = ServiceProviderstausSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'address', 'city', 'state', 'country', 'postal_code', 'profile_pic','service_provider_info']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def get_service_image(self, obj):
        request = self.context.get('request')
        if obj.profile_pic and hasattr(obj.profile_pic, 'url'):
            return request.build_absolute_uri(obj.profile_pic.url)
        return None



# serializers.py
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_type', 'service_description', 'service_image', 'service_price']

    def get_service_image(self, obj):
        request = self.context.get('request')
        if obj.service_image and hasattr(obj.service_image, 'url'):
            return request.build_absolute_uri(obj.service_image.url)
        return None

    def validate_service_name(self, value):
        if not value:
            raise serializers.ValidationError("Service name is required.")
        return value

    def validate_service_type(self, value):
        if not value:
            raise serializers.ValidationError("Service type is required.")
        return value

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
