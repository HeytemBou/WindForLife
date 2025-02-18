# Django imports
from django.http import HttpRequest
from django.contrib.auth import get_user_model, authenticate

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status

# Serializers
from apps.anemometers.api.v1.serializers import AnemometerMeasurementSerializer


class AnemometerMeasurementsUseCase:
    """
    Usecase class that contains the logic to create an anemometer
    """
    def __init__(self, request_data: dict):
        self.request_data = request_data
        self.serializer = AnemometerMeasurementSerializer(data=request_data)

    def execute(self) -> Response:

        # Check if the serializer is valid
        if not self.serializer.is_valid():
            return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the anemometer
        self.serializer.save()

        return Response("Wind measurement submitted successfully", status=status.HTTP_201_CREATED)


        
