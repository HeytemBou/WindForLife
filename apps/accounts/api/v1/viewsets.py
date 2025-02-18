
# rest framework imports
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

# Model imports
from apps.accounts.models.account import Account

# Services imports
from apps.accounts.api.v1.services.sign_up_usecase import SignUpUseCase
from apps.accounts.api.v1.services.sign_in_usecase import SignInUseCase


class AccountsViewSet(viewsets.ViewSet):
    """Viewset for the User Sign Up API"""

    queryset = Account.objects.all()

    # Account sign up api
    @action(detail=False, methods=["POST"], url_path="v1/sign-up", permission_classes=[permissions.AllowAny])
    def account_sign_up(self, request, *args, **kwargs):
        """
        """
        # specify the permission and authentication classes
        self.permission_classes = [permissions.AllowAny]

        # Instantiate the usecase
        usecase = SignUpUseCase(request)
        return usecase.execute()

    @action(detail=False, methods=["POST"], url_path="v1/sign-in", permission_classes=[permissions.AllowAny])
    def account_sign_in(self, request, *args, **kwargs):
        """
        This method is used to authenticate a user
        """
        # specify the permission and authentication classes
        self.permission_classes = [permissions.AllowAny]

        # Instantiate the usecase
        usecase = SignInUseCase(request)
        return usecase.execute()
