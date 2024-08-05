from typing import Final
from django.conf import settings


class Constants(object):
    MESSAGE_OK: str = "Data processed successfully"
    MESSAGE_CREATED: str = "Data created successfully"
    MESSAGE_UPDATED: str = "Data updated successfully"
    MESSAGE_DELETED: str = "Data deleted successfully"
    MESSAGE_ERROR: str = "An error occurred while processing the data"
    MESSAGE_NOT_FOUND: str = "Data not found"
    MESSAGE_BAD_REQUEST: str = "Bad request"
    MESSAGE_UNAUTHORIZED: str = "Unauthorized"
    MESSAGE_FORBIDDEN: str = "Forbidden"
    MESSAGE_METHOD_NOT_ALLOWED: str = "Method not allowed"
    PROTOCOL: str = "http"
    STATE_CHOICES = (
        ("Aguascalientes", "Aguascalientes"),
        ("Baja California", "Baja California"),
        ("Baja California Sur", "Baja California Sur"),
        ("Campeche", "Campeche"),
        ("Coahuila de Zaragoza", "Coahuila de Zaragoza"),
        ("Colima", "Colima"),
        ("Chiapas", "Chiapas"),
        ("Chihuahua", "Chihuahua"),
        ("CDMX", "CDMX"),
        ("Durango", "Durango"),
        ("Guanajuato", "Guanajuato"),
        ("Guerrero", "Guerrero"),
        ("Hidalgo", "Hidalgo"),
        ("Jalisco", "Jalisco"),
        ("México", "México"),
        ("Michoacán de Ocampo", "Michoacán de Ocampo"),
        ("Morelos", "Morelos"),
        ("Nayarit", "Nayarit"),
        ("Nuevo León", "Nuevo León"),
        ("Oaxaca", "Oaxaca"),
        ("Puebla", "Puebla"),
        ("Querétaro", "Querétaro"),
        ("Quintana Roo", "Quintana Roo"),
        ("San Luis Potosí", "San Luis Potosí"),
        ("Sinaloa", "Sinaloa"),
        ("Sonora", "Sonora"),
        ("Tabasco", "Tabasco"),
        ("Tamaulipas", "Tamaulipas"),
        ("Tlaxcala", "Tlaxcala"),
        ("Veracruz de Ignacio de la Llave", "Veracruz de Ignacio de la Llave"),
        ("Yucatán", "Yucatán"),
        ("Zacatecas", "Zacatecas"),
    )

    TIPOS_LICENCIAS = (
        ("Licencia conducir", "Licencia conducir"),
        ("Licencia material peligroso", "Licencia material peligroso"),
    )
    
    API_BASE_PATH: Final[str] = f"api/{settings.API_VERSION}/"
    URL_CLIENTE: Final[str] = f"clientes"
    URL_TRANSPORTISTA: Final[str] = f"transportistas"
    URL_USUARIO: Final[str] = f"usuarios"

    if settings.ENVIRONMENT == "local":
        FRONTED_URL: Final[str] = "http://localhost:3000"
    elif settings.ENVIRONMENT == "development":
        FRONTED_URL: Final[str] = "http://74.208.98.114"
        
constants = Constants()
