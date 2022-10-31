from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        
        model = User
        USERNAME_FIELD = 'USERNAME OR PASSWORD'
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')
