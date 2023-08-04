from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=64,
        )
    
    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            is_active = False,
            )
                        
        return user
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')