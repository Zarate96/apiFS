from rest_framework import serializers
from .models import MyUser, DatosFiscales, Cliente, Transportista
from django.db import transaction
from django.contrib.auth.hashers import make_password 


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "email",
            "password",
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

        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        # Validate if the user is either client or transportista
        if not client and not transportista:
            raise serializers.ValidationError("El usuario debe ser cliente o transportista")
        if client and transportista:
            raise serializers.ValidationError("El usuario no puede ser cliente y transportista al mismo tiempo")

        # Create the user instance
        if client:
            user = MyUser.objects.create(is_active=False, es_cliente=True, **validated_data)
        if transportista:
            user = MyUser.objects.create(is_active=False, es_transportista=True, **validated_data)
       

        # Create corresponding objects based on user type
        if client:
            Cliente.objects.create(user=user)
        elif transportista:
            Transportista.objects.create(user=user)

        # Create DatosFiscales instance
        DatosFiscales.objects.create(user=user, es_empresa=moral)

        return user