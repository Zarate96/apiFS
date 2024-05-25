from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers, generics
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django_filters import rest_framework as filters

from accounts.models import MyUser
from .models import Transportistas, LicenciasTransportistas, Unidades, Encierros
from .serializers import (
    TransportistaSerializer,
    LicenciasTransportistasSerializer,
    UnidadesSerializer,
    EncierroSerializer,
    UnidadesSerializer,
)
from .filters import EncierroFilter

from shared.permissions import IsOwner, IsTransportista
from shared.schemas.responses import custom_response
from shared.constants import constants


class TransportistaAPIView(APIView):
    """
    API view for transportista.
    """

    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, slug=None) -> Response:
        """
        Handle GET requests for transportista.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = TransportistaSerializer(user.transportista)
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request, slug=None) -> Response:
        """
        Handle PATCH requests for transportista.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = TransportistaSerializer(
                user.transportista, data=request.data, partial=True
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


class LicenciasTransportistasAPIView(APIView):
    """
    API view for LicenciasTransportistas.
    """

    permission_classes = [IsAuthenticated, IsOwner, IsTransportista]

    def get(self, request, slug=None) -> Response:
        """
        Handle GET requests for LicenciasTransportistas.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            if (
                user.transportista.has_licencia_conducir
                and "licencia-conducir" in request.path
            ):
                serializer = LicenciasTransportistasSerializer(
                    LicenciasTransportistas.objects.get(
                        user=user.transportista, tipo_licencia="Licencia conducir"
                    )
                )
            elif user.transportista.has_licencia_mp and "licencia-mp" in request.path:
                serializer = LicenciasTransportistasSerializer(
                    LicenciasTransportistas.objects.get(
                        user=user.transportista,
                        tipo_licencia="Licencia material peligroso",
                    )
                )
            else:
                raise ValidationError("El transportista no cuenta con esta licencia")
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request, slug=None) -> Response:
        """
        Handle PATCH requests for LicenciasTransportistas.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = LicenciasTransportistasSerializer(
                user.transportista.licenciastransportistas,
                data=request.data,
                partial=True,
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
            data = str
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def post(self, request, slug=None) -> Response:
        """
        Handle POST requests to create LicenciasTransportistas.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)

            serializer = LicenciasTransportistasSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tipo_licencia = request.data.get("tipo_licencia")
            if (
                tipo_licencia == "Licencia conducir"
                and user.transportista.has_licencia_conducir
            ):
                raise ValidationError(
                    "El transportista ya tiene una licencia de conducir"
                )
            if (
                tipo_licencia == "Licencia material peligroso"
                and user.transportista.has_licencia_mp
            ):
                raise ValidationError(
                    "El transportista ya tiene una licencia de material peligroso"
                )

            serializer.save(user=user.transportista)
            data = serializer.data
            status_code = status.HTTP_201_CREATED
            message = constants.MESSAGE_CREATED

        except (serializers.ValidationError, ValidationError) as ve:
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.MESSAGE_BAD_REQUEST
            data = str(ve)

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
            data = str(e)

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


class UnidadesAPIView(APIView):
    """
    API view for Unidades.
    """

    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, slug=None) -> Response:
        """
        Handle GET requests for Unidades.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = UnidadesSerializer(user.transportista.unidades)
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request, slug=None) -> Response:
        """
        Handle PATCH requests for Unidades.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = UnidadesSerializer(
                user.transportista.unidades, data=request.data, partial=True
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


class ListEncierrosAPIView(generics.ListAPIView):
    """
    API view for list of Encierros.
    """

    serializer_class = EncierroSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsTransportista]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EncierroFilter

    def get_queryset(self):
        user_slug = self.kwargs.get("slug")
        user = get_object_or_404(MyUser, slug=user_slug)
        self.check_object_permissions(self.request, user)
        if not user.transportista.has_encierro:
            raise PermissionDenied("El transportista no cuenta con encierros")
        return Encierros.objects.filter(user=user.transportista)

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


class EncierroAPIView(APIView):
    """
    API view for Encierro.
    """

    permission_classes = [IsAuthenticated, IsOwner, IsTransportista]
    
    def get(self, request, slug=None, encierro_slug=None) -> Response:
        """
        Handle GET requests for Encierro.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            encierro = get_object_or_404(Encierros, slug=encierro_slug)
            serializer = EncierroSerializer(encierro)
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Http404:
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
            data = constants.MESSAGE_NOT_FOUND
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def post(self, request, slug=None) -> Response:
        """
        Handle POST requests to create Encierro.
        """
        try:
            print("entra")
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = EncierroSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user.transportista)
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
        except IntegrityError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "El encierro ya existe para este transportista"
            data = str(e)
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.MESSAGE_ERROR
            data = str(e)
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request, slug=None, encierro_slug=None) -> Response:
        """
        Handle PATCH requests for Encierro.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            encierro = get_object_or_404(Encierros, slug=encierro_slug)
            serializer = EncierroSerializer(encierro, data=request.data, partial=True)
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
        except IntegrityError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Este nombre de encierro ya existe para este transportista"
            data = str(e)
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.MESSAGE_ERROR
            data = str(e)
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)


class ListUnidadesAPIView(generics.ListAPIView):
    """
    API view for list of Unidades.
    """

    serializer_class = UnidadesSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsTransportista]

    def get_queryset(self):
        user_slug = self.kwargs.get("slug")
        user = get_object_or_404(MyUser, slug=user_slug)
        self.check_object_permissions(self.request, user)
        if not user.transportista.has_unidades:
            raise PermissionDenied("El transportista no cuenta con unidades")
        return Unidades.objects.filter(user=user.transportista)

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


class UnidadesAPIView(APIView):
    """
    API view for Unidades.
    """

    permission_classes = [IsAuthenticated, IsOwner, IsTransportista]

    def get(self, request, placa=None, slug=None) -> Response:
        """
        Handle GET requests for Unidades.
        """
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            unidad = get_object_or_404(Unidades, placa=placa)
            self.check_object_permissions(request, user)
            serializer = UnidadesSerializer(unidad)
            data = serializer.data
        except PermissionDenied as e:
            data = str(e)
            status_code = status.HTTP_403_FORBIDDEN
            message = constants.MESSAGE_FORBIDDEN
        except Exception as e:
            data = str(e)
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

    def patch(self, request, slug=None, placa=None) -> Response:
        """
        Handle PATCH requests for Unidades.
        """
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            unidad = get_object_or_404(Unidades, placa=placa)
            serializer = UnidadesSerializer(
                unidad, data=request.data, partial=True
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
    
    def post(self, request, slug=None) -> Response:
        '''
        Handle POST requests for Unidades.
        '''
        try:
            user = get_object_or_404(MyUser, slug=slug)
            self.check_object_permissions(request, user)
            serializer = UnidadesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user.transportista)
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
        except IntegrityError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "La unidad ya existe para este transportista"
            data = str(e)
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.MESSAGE_ERROR
            data = str(e)
        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)