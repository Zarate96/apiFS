from rest_framework import serializers
from .models import MyUser, DatosFiscales, Cliente
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
        validated_data['password'] = make_password(validated_data['password'])
        user = MyUser.objects.create(is_active=False, **validated_data)

        DatosFiscales.objects.create(user=user, es_empresa=moral)

        if client:
            Cliente.objects.create(user=user)

        if transportista:
            pass

        return user
