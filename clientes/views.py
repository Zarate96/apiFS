from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django_filters import rest_framework as filters

from accounts.models import MyUser
from .models import Domicilios
from .serializers import ClienteSerializer, DomiciliosSerializer
from .filters import DomiciliosFilter

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
            serializer.is_valid(raise_exception=True)
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


class DomiciliosListAPIView(generics.ListAPIView):
    serializer_class = DomiciliosSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsCliente]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DomiciliosFilter

    def get_queryset(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        if not user.clientes.has_domicilios:
            raise PermissionDenied("El cliente no cuenta con domicilios")
        return Domicilios.objects.filter(user=user.clientes)

    def list(self, request, *args, **kwargs):
        response_data = {}
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            response_data = custom_response(
                serializer.data, status.HTTP_200_OK, constants.MESSAGE_OK
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except PermissionDenied as e:
            response_data = custom_response(
                str(e), status.HTTP_403_FORBIDDEN, constants.MESSAGE_FORBIDDEN
            )
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            response_data = custom_response(
                str(e), status.HTTP_500_INTERNAL_SERVER_ERROR, constants.MESSAGE_ERROR
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DomiciliosAPIView(APIView):
    """
    API view for client addresses.
    """

    permission_classes = [IsAuthenticated, IsOwner, IsCliente]

    def get(self, request, slug=None) -> Response:
        """
        Handle GET requests for client addresses.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = request.user
            self.check_object_permissions(request, user)
            domicilio = get_object_or_404(Domicilios, slug=slug)
            if domicilio.user != user.clientes:
                raise PermissionDenied("El domicilio no pertenece a este cliente")
            serializer = DomiciliosSerializer(domicilio)
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

    def patch(self, request, slug=None) -> Response:
        """
        Handle PATCH requests for client addresses.
        """
        try:
            user = request.user
            self.check_object_permissions(request, user)
            domicilio = get_object_or_404(Domicilios, slug=slug)
            if domicilio.user != user.clientes:
                raise PermissionDenied("El domicilio no pertenece a este cliente")
            serializer = DomiciliosSerializer(
                domicilio, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
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

    def post(self, request) -> Response:
        """
        Handle POST requests for client addresses.
        """
        try:
            user = request.user
            self.check_object_permissions(request, user)
            serializer = DomiciliosSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user.clientes)
            data = serializer.data
            status_code = status.HTTP_201_CREATED
            message = constants.MESSAGE_CREATED
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
