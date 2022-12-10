from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        
        model = User
        USERNAME_FIELD = 'USERNAME OR PASSWORD'
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(username = validated_data['username'], email = validated_data['email'], first_name = validated_data['first_name'], last_name  = validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.save()

        #user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], validated_data['first_name'], validated_data['last_name'])

        return user

