from rest_framework import serializers
from .utils import validate_address, validate_address_for_domicilios
from .models import Clientes, Domicilios


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
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
        try:
            validated_address = validate_address(address_str)
            instance.direccion_google = validated_address
            instance.save()
            instance = super().update(instance, validated_data)
        except serializers.ValidationError as ve:
            raise ve

        return instance


class DomiciliosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilios
        exclude = ["user"]

    def build_address_string(self, validated_data):
        """
        Build a formatted address string from the validated data.
        """
        print("build_address_string")
        address_components = {
            "street": validated_data.get("calle"),
            "number": validated_data.get("num_ext"),
            "neighborhood": validated_data.get("colonia"),
            "city": validated_data.get("municipio"),
            "state": validated_data.get("estado"),
            "postal_code": validated_data.get("cp"),
        }
        return ", ".join(
            value for key, value in address_components.items() if value is not None
        )

    def validate_address_domicilios(self, validated_data):
        """
        Validate the given address using an external validation service.
        """
        print("validate_address_domicilios")
        address_str = self.build_address_string(validated_data)
        print(address_str)
        return validate_address_for_domicilios(address_str)

    def update_validated_data(self, validated_data, address_dict):
        """
        Update validated data with address validation results.
        """
        validated_data.update({
            "es_valida": address_dict["es_valida"],
            "formato_google": address_dict["formato_google"],
            "latitud": address_dict["latitud"],
            "longitud": address_dict["longitud"],
            "id_google": address_dict["id_google"]
        })

    def create(self, validated_data):
        """
        Create a new Domicilios instance after validating the address.
        """
        address_dict = self.validate_address_domicilios(validated_data)
        self.update_validated_data(validated_data, address_dict)
        return Domicilios.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Domicilios instance after validating the address.
        """
        address_dict = self.validate_address_domicilios(validated_data)
        print(address_dict)
        self.update_validated_data(validated_data, address_dict)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance