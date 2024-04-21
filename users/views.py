from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils import send_activation_email
from .serializers import MyUserSerializer
from .schemas.responses import custom_response
from constants import constants
from .models import Cliente, MyUser
from django.shortcuts import get_object_or_404
from .permissions import IsOwner
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class UserAPIView(APIView):
    """
    API view for user registration.
    """

    def post(self, request) -> Response:
        """
        Handle POST requests for user registration.
        """
        try:
            serializer = MyUserSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                status_code = status.HTTP_201_CREATED
                message = constants.MESSAGE_CREATED
                data = serializer.data
                try:
                    send_activation_email(user, self.request)
                    print("send_activation_email")
                except Exception as e:
                    message = constants.MESSAGE_ERROR
                    return Response(
                        custom_response(
                            {}, status.HTTP_500_INTERNAL_SERVER_ERROR, message
                        ),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                message = constants.MESSAGE_BAD_REQUEST
                data = serializer.errors
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)
        except Exception as e:
            message = constants.MESSAGE_ERROR
            return Response(
                custom_response({}, status.HTTP_500_INTERNAL_SERVER_ERROR, message),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserDetailApiView(APIView):
    """
    API view for user profile.
    """

    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, slug=None) -> Response:
        status_code = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        data = {}
        try:
            user = get_object_or_404(MyUser, slug=slug)
            serializer = MyUserSerializer(user)
            try:
                self.check_object_permissions(request, user)
                data = serializer.data
            except:
                status_code = status.HTTP_403_FORBIDDEN
                message = constants.MESSAGE_FORBIDDEN

        except:
            status_code = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND

        finally:
            response_data = custom_response(data, status_code, message)
            return Response(response_data, status=status_code)

class ActivateUserApiView(APIView):
    """
    API view for user activation.
    """

    def get(self, request, uidb64=None, token=None) -> Response:
        """
        Handle GET requests for user activation.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
        except Exception as e:
            return Response(
                custom_response({}, status.HTTP_500_INTERNAL_SERVER_ERROR, e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user.is_active = True
        user.save()

        response_data = custom_response({}, status=status.HTTP_200_OK, message="User activated successfully")
        return Response(response_data, status=status.HTTP_200_OK)