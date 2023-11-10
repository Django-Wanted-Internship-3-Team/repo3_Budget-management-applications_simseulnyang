from rest_framework import serializers

from budget_management.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ("username", "created_at", "updated_at")


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
