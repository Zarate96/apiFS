from rest_framework import serializers
from shared.utils import validate_address

from .models import Transportistas, LicenciasTransportistas, Unidades, Encierros, Unidades
from clientes.utils import validate_address


class TransportistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportistas
        exclude = [
            "user",
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
        print(address_str)
        try:
            validated_address = validate_address(address_str)
            instance.direccion_google = validated_address
            instance.save()
            instance = super().update(instance, validated_data)
        except serializers.ValidationError as ve:
            raise ve

        return instance


class LicenciasTransportistasSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenciasTransportistas
        exclude = [
            "user",
        ]

    def create(self, validated_data):
        image = validated_data.get("licencia_foto")
        if image.size > 5242880:
            raise serializers.ValidationError("La imagen es demasiado grande")
        return super().create(validated_data)


class UnidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidades
        exclude = [
            "user",
        ]


class EncierroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encierros
        exclude = ["user"]

    def validate_address(self, validated_data):
        address_components = {
            "street": validated_data.get("calle"),
            "number": validated_data.get("num_ext"),
            "neighborhood": validated_data.get("colonia"),
            "city": validated_data.get("municipio"),
            "state": validated_data.get("estado"),
            "postal_code": validated_data.get("cp"),
        }
        address_str = ", ".join(
            value for key, value in address_components.items() if value is not None
        )
        validated_address = validate_address(address_str)
        return validated_address

    def create(self, validated_data):
        validated_data["direccion_google"] = self.validate_address(validated_data)
        instance = Encierros.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["direccion_google"] = self.validate_address(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UnidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidades
        exclude = [
            "user",
        ]
    