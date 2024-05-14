from rest_framework import serializers
from .utils import validate_address
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
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