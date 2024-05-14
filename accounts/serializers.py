from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from rest_framework import serializers

from .models import MyUser, DatosFiscales
from .utils import send_reset_email

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

    def validate(self, attrs):
        email = attrs.get("email")
        user = MyUser.objects.filter(email=email).first()
        if user is not None:
            try:
                request = self.context["request"]
                send_reset_email(user, request)
            except Exception as e:
                raise serializers.ValidationError(str(e))
            return attrs
        else:
            raise serializers.ValidationError("You are not a Registered User")
        


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
    