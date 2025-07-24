from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'national_code', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'phone': {'required': True, 'allow_blank': False},
            'national_code': {'required': True, 'allow_blank': False},
            'username': {'required': False, 'allow_blank': True},
        }

    def validate_national_code(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("National code must be 10 digits.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
