# Django imports
from django.http import HttpRequest
from django.contrib.auth import authenticate

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status

# Serializers
from apps.accounts.api.v1.serializers import AccountSignInSerializer

# Utils
from utils.security.jwt_utils import create_access_token, create_refresh_token


class SignInUseCase:
    """
    Usecase class that contains the logic to authenticate a user
    """

    def __init__(self, request: HttpRequest):
        self.request = request
        self.serializer = AccountSignInSerializer(data=request.data)

    def execute(self) -> Response:

        # Validate the request data
        if not self.serializer.is_valid():
            return Response({
                "ERROR": "BAD_REQUEST",
                "DETAILS": self.serializer.errors,
            },
                status=status.HTTP_400_BAD_REQUEST)

        # Get the email and password from the serializer
        email: str = self.serializer.validated_data.get('email')
        password: str = self.serializer.validated_data.get('password')

        # Authenticate the user
        account = authenticate(email=email, password=password)
        if account is None:
            return Response({"error": "INVALID_EMAIL_OR_PASSWORD"}, status=status.HTTP_401_UNAUTHORIZED)

        # Create the access and refresh tokens
        access_token = create_access_token(str(account.id))
        refresh_token = create_refresh_token(str(account.id))

        return Response({"message": "Logged in successfully",
                         "details": {
                             "account_id": account.id,
                             "access_token": access_token,
                             "refresh_token": refresh_token,
                         }
                         },
                        status=201)
