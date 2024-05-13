from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MyUser
from .utils import send_activation_email
from .schemas.responses import custom_response
from .serializers import MyUserSerializer, UserLoginSerializer, SendPasswordResetEmailSerializer

from shared.constants import constants


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


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

        response_data = custom_response(
            {}, status=status.HTTP_200_OK, message="User activated successfully"
        )
        return Response(response_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    """
    API view for user login.
    """

    def post(self, request, format=None) -> Response:
        status_response = status.HTTP_200_OK
        message = constants.MESSAGE_OK
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            if user is not None:
                data = get_tokens_for_user(user)
            else:
                status_response = status.HTTP_404_NOT_FOUND
                message = constants.MESSAGE_NOT_FOUND
                data = {
                    "errors": {
                        "non_field_errors": ["Username or Password is not valid"]
                    }
                }
        except Exception as e:
            status_response = status.HTTP_404_NOT_FOUND
            message = constants.MESSAGE_NOT_FOUND
            data = str(e)
        response_data = custom_response(data, status=status_response, message=message)
        return Response(response_data, status=status_response)


class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )
