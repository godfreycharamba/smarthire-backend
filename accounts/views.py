from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UpdateUserSerializer,
    ChangePasswordSerializer
)

from common.views import BaseAPIView
from .serializers import LoginSerializer


class RegisterView(BaseAPIView, CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(
                message="Registration failed",
                data=serializer.errors
            )

        self.perform_create(serializer)

        return self.success_response(
            data=serializer.data,
            message="User registered successfully",
            status_code=201
        )


class LoginView(BaseAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(
                message="Invalid email or password",
                status_code=401
            )

        return self.success_response(
            data=serializer.validated_data,
            message="Login successful"
        ) 
    

class UserRetrieveView(BaseAPIView, RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return self.success_response(
            data=serializer.data,
            message="User retrieved successfully"
        )


# -------------------------
# Update user (PUT/PATCH)
# -------------------------
class UserUpdateView(BaseAPIView, UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return self.error_response(
                message="Update failed",
                data=serializer.errors
            )

        self.perform_update(serializer)

        return self.success_response(
            data=serializer.data,
            message="User updated successfully"
        )
    
class ChangePasswordView(BaseAPIView, GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(
                message="Invalid data",
                data=serializer.errors,
                status_code=400
            )

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(old_password):
            return self.error_response(
                message="Old password is incorrect",
                status_code=400
            )

        user.set_password(new_password)
        user.save()

        return self.success_response(
            data=None,
            message="Password changed successfully"
        ) 


# -------------------------
# Delete user (DELETE)
# -------------------------
class UserDeleteView(BaseAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())

        return self.success_response(
            data=None,
            message="User deleted successfully"
        )   
