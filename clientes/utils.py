import googlemaps
from django.conf import settings 
from rest_framework import serializers

gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

def validate_address(address) -> str:
    """
    Validate the given address using Google Maps API.
    """
    geocode_result = gmaps.geocode(address)
    try:
        direccion_google = geocode_result[0]["formatted_address"]
        if len(geocode_result) == 0 or len(direccion_google) < 50:
            raise serializers.ValidationError(f"The address {address} is not valid")
        return direccion_google
    except Exception as e:
        raise serializers.ValidationError(str(e))
