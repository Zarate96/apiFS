from rest_framework import serializers
from .models import MyUser, DatosFiscales, Cliente, Transportista, DatosFiscales
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .utils import validate_address


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


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = [
            "user",
            "conektaId",
            "es_validado",
            "file_import",
            "direccion_google",
        ]

    def update(self, instance, validated_data):
        address_components = {
            "street": validated_data.get("calle"),
            "number": validated_data.get("num_ext"),
            "neighborhood": validated_data.get("colonia"),
            "city": validated_data.get("municipio"),
            "state": validated_data.get("estado"),
            "postal_code": validated_data.get("cp"),
        }
        # Construct the full address string
        address_str = ", ".join(
            value for key, value in address_components.items() if value is not None
        )
        try:
            validated_address = validate_address(address_str)
            # Update the instance with validated data and save validated address to direccion_google field
            instance.direccion_google = validated_address
            instance.save()
            instance = super().update(instance, validated_data)
        except serializers.ValidationError as ve:
            raise ve

        return instance

class DatosFiscalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFiscales
        exclude = ["direccion_google","es_empresa","user","verificador_foto","es_verificado"]

    def update(self, instance, validated_data):
        address_components = {
            "street": validated_data.get("calle"),
            "number": validated_data.get("num_ext"),
            "neighborhood": validated_data.get("colonia"),
            "city": validated_data.get("municipio"),
            "state": validated_data.get("estado"),
            "postal_code": validated_data.get("cp"),
        }
        # Construct the full address string
        address_str = ", ".join(
            value for key, value in address_components.items() if value is not None
        )
        try:
            validated_address = validate_address(address_str)
            # Update the instance with validated data and save validated address to direccion_google field
            instance.direccion_google = validated_address
            instance.save()
            instance = super().update(instance, validated_data)
        except serializers.ValidationError as ve:
            raise ve

        return instance