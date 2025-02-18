# Standard imports
from datetime import timezone

# rest framework imports
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Django imports
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction, IntegrityError, DatabaseError, Error

# Local imports
from apps.anemometers.models import Anemometer, AnemometerTag

# Services imports
from WindForLife.apps.anemometers.api.v1.services.submit_anemometer_measurements_usecase import AnemometerCreateUseCase
from apps.anemometers.api.v1.services.delete_anemometer_usecase import AnemometerDeleteUseCase
from apps.anemometers.api.v1.services.list_anemometers_usecase import AnemometerListUseCase

# Utils imports
from utils.security.jwt_authentication import JWTAuthentication


class AneomometerViewset(viewsets.ViewSet):
    """Viewset for the User Sign Up API"""

    queryset = Anemometer.objects.all()

    # Anemometer create api
    @action(methods=['post'], url_path="v1/anemometers",detail=False, authentication_classes=[JWTAuthentication])
    def create_anemometer(self, request):
        """
        API to create anemometer
        """
        # Instantiate the usecase
        usecase = AnemometerCreateUseCase(request)
        # Execute the usecase
        response = usecase.execute()
        return response
    
    
    # Anemometer delete api
    @action(methods=['delete'], url_path="v1/anemometers/(?P<id>[^/.]+)",detail=False, authentication_classes=[JWTAuthentication])
    def delete_anemometer(self, request, id: str):
        """
        API to delete anemometer
        """
        # Instantiate the usecase
        request.data['id'] = id
        usecase = AnemometerDeleteUseCase(request)
        # Execute the usecase
        response = usecase.execute()

        return response

    # Anemometer list api
    @action(methods=['get'], url_path="v1/anemometers/list", detail=False, authentication_classes=[JWTAuthentication])
    def list_anemometers(self, request):
        """
        API to list anemometers with pagination
        """
        # Instantiate the usecase
        usecase = AnemometerListUseCase(request)
        # Execute the usecase
        response = usecase.execute()
        return response


    # Anemometer update api
    @action(methods=['put'], url_path="v1/anemometers", detail=True, authentication_classes=[JWTAuthentication])
    def update_anemometer(self, request):
        """
        API to update anemometer
        """
        pass

    # Submit anemometer measurements for a given anemometer
    @action(methods=['post'], url_path="v1/anemometers/(?P<id>[^/.]+)/measurements", detail=False, authentication_classes=[JWTAuthentication])
    def submit_anemometer_measurements(self, request):
        """
        API to submit anemometer measurements
        """
        pass
       
       
    
   