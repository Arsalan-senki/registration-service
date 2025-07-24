# serializers.py: Serializers for user registration and validation
from rest_framework import serializers
from .models import User

# Serializer for registering a new user
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be included in the registration process
        fields = ['id', 'username', 'first_name', 'last_name', 'national_code', 'phone', 'password']
        extra_kwargs = {
            # Password should only be writeable, not readable
            'password': {'write_only': True},
            # The following fields are required and cannot be blank
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'phone': {'required': True, 'allow_blank': False},
            'national_code': {'required': True, 'allow_blank': False},
            # Username is optional and can be blank
            'username': {'required': False, 'allow_blank': True},
        }

    # Custom validator for the national_code field
    def validate_national_code(self, value):
        # National code must be exactly 10 digits
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("National code must be 10 digits.")
        return value

    # Overriding create to handle password hashing
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
