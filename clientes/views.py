from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from accounts.models import MyUser
from .serializers import ClienteSerializer

from shared.permissions import IsOwner, IsCliente
from shared.schemas.responses import custom_response
from shared.constants import constants

class ClienteAPIView(APIView):
    """
    API view for client.
    """

    permission_classes = [IsAuthenticated, IsOwner, IsCliente]

    def get(self, request) -> Response:
        """
        Handle GET requests for client.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = request.user
            self.check_object_permissions(request, user)
            serializer = ClienteSerializer(user.clientes)
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.MESSAGE_ERROR
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request) -> Response:
        """
        Handle PATCH requests for client.
        """
        try:
            user = request.user
            self.check_object_permissions(request, user)
            serializer = ClienteSerializer(
                user.clientes, data=request.data, partial=True
            )
            serializer.is_valid(
                raise_exception=True
            )  
            serializer.save()
            data = serializer.data
            status_code = status.HTTP_200_OK
            message = constants.MESSAGE_UPDATED
        except serializers.ValidationError as ve:
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.MESSAGE_BAD_REQUEST
            data = str(ve)
        except ValidationError as ve:
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.MESSAGE_BAD_REQUEST
            data = str(ve)
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Http404:
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
            data = constants.MESSAGE_NOT_FOUND
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.MESSAGE_ERROR
            data = str(e)
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)