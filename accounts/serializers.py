from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import MyUser, DatosFiscales

from clientes.models import Cliente
from transportistas.models import Transportista


class MyUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "es_empresa",
            "es_transportista",
            "es_cliente",
            "es_verificador",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        moral = validated_data.pop("es_empresa", False)
        client = validated_data.pop("es_cliente", False)
        transportista = validated_data.pop("es_transportista", False)
        password2 = validated_data.pop("password2")

        # Validate if passwords match
        if validated_data["password"] != password2:
            raise serializers.ValidationError("Passwords do not match")

        # Hash the password
        validated_data["password"] = make_password(validated_data["password"])

        # Validate if the user is either client or transportista
        if not client and not transportista:
            raise serializers.ValidationError(
                "El usuario debe ser cliente o transportista"
            )
        if client and transportista:
            raise serializers.ValidationError(
                "El usuario no puede ser cliente y transportista al mismo tiempo"
            )

        # Create the user instance
        if client:
            user = MyUser.objects.create(
                is_active=False, es_cliente=True, **validated_data
            )
        if transportista:
            user = MyUser.objects.create(
                is_active=False, es_transportista=True, **validated_data
            )

        # Create corresponding objects based on user type
        if client:
            Cliente.objects.create(user=user)
        elif transportista:
            Transportista.objects.create(user=user)

        # Create DatosFiscales instance
        DatosFiscales.objects.create(user=user, es_empresa=moral)

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Username or Password is not valid")

        else:
            raise serializers.ValidationError("Both username and password are required")

        attrs["user"] = user
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]
