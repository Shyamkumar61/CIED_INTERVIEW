from markdown.extensions.toc import unique
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.account.models import Account

User = get_user_model()


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(write_only=True)


class CreateMedBillAccountSerializer(serializers.Serializer):

    ROLE_CHOICES = (
        ("med_staff", "Medical Staff"),
        ("inventory_manager", "Inventory Manager"),
    )

    email = serializers.EmailField(max_length=200, required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(
        write_only=True,
        required=True,
        style={
            "input_type": "text",
            "placeholder": "First Name",
        },
    )
    last_name = serializers.CharField(
        write_only=True,
        required=True,
        style={
            "input_type": "text",
            "placeholder": "Last Name",
        },
    )
    role = serializers.ChoiceField(
        required=True,
        choices=ROLE_CHOICES,
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists")
        for field_name, field_value in attrs.items():
            if field_value is None:
                raise serializers.ValidationError(f"{field_name} is required")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_medBill_user(**validated_data)
        return user


class AccountSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=200, read_only=True)

    class Meta:
        model = Account
        fields = ("id", "first_name", "last_name", "email", "role")
