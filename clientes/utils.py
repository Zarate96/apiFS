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


def validate_address_for_domicilios(address) -> dict:
    """
    Validate the given address using Google Maps API.
    """
    data = {}
    
    try:
        print(address)
        geocode_result = gmaps.geocode(address)
        direccion_google = geocode_result[0]["formatted_address"]
        if len(geocode_result) == 0 or len(direccion_google) < 50:
            data['es_valida'] = False
            data['formato_google'] = "Invalid"
            data['latitud'] = 0
            data['longitud'] = 0
            data['id_google'] = "not valid"
            data['formato_google'] = "not valid"
        else:
            data['latitud'] = geocode_result[0]["geometry"]["location"]["lat"]
            data['longitud'] = geocode_result[0]["geometry"]["location"]["lng"]
            data['id_google'] = geocode_result[0]["place_id"]
            data['formato_google'] = direccion_google
            data['es_valida'] = True
        print(data)
        return data
    except Exception as e:
        raise serializers.ValidationError(str(e))
    
