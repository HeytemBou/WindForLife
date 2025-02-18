# Django imports
from django.http import HttpRequest

# Rest framework imports
from rest_framework.response import Response

# Serializers
from apps.accounts.api.v1.serializers import AccountSignUpSerializer

# Models
from apps.accounts.models.account import Account

# Utils
from utils.security.jwt_utils import create_access_token, create_refresh_token

class SignUpUseCase:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.serializer = AccountSignUpSerializer(data=request.data)

    def execute(self) -> Response:
        
        # First we need to validate the request using the serializer
        if not self.serializer.is_valid():
            return Response({
                                "ERROR": "BAD_REQUEST",
                                "DETAILS": self.serializer.errors,
                            }, 
                            status=400)
        
        # Check if the email is already in use
        if Account.objects.filter(email=self.request.data.get('email')).exists():
            return Response({
                                "ERROR": "EMAIL_ALREADY_IN_USE",
                            }, 
                            status=400)
        # Save the account
        account=self.serializer.save()
        print("Account created successfully")
        print(account.id)
        print(account.email)

        # Generate an access and a refresh token
        access_token: str = create_access_token(str(account.id))
        refresh_token: str = create_refresh_token(str(account.id))

        return Response({ "message": "Account created successfully",
                          "details": {
                            "account_id": account.id,
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            }
                        }, 
                        status=201)