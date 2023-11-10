from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from budget_management.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "created_at", "updated_at")


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        if user is not None:
            refresh = TokenObtainPairSerializer.get_token(user)
            refresh["username"] = user.username
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return data
        return None

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])

        if user is None or not user.is_active:
            raise serializers.ValidationError("Username or Password is Incorrect")

        data["token"] = self.get_token(user)

        return data
