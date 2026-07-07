from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "registration_date",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "registration_date",
        ]


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
                "phone_number": user.phone_number,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }  
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({
                "message": "New passwords do not match"
            })

        return attrs    