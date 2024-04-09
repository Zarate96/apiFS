from rest_framework.exceptions import ValidationError
from rest_framework import status

def custom_response(user_data=dict, status=str, message=str) -> dict:
    return {
        'code': status,
        'message': message,
        'data': user_data
    }

class CustomValidationError(ValidationError):
    def get_error_response(self):
        data = super().get_error_response()
        data['code'] = status.HTTP_400_BAD_REQUEST
        return data

