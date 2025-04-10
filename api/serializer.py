from accounts.models import *
from rest_framework import serializers as Serializers

class UserSerializer(Serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")