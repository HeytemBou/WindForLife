# Standard imports
from typing import Optional

# Django imports
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

# Models
from apps.anemometers.models.anemometer import Anemometer

# Validators
from apps.anemometers.api.v1.validators import validate_limit_and_offset


class MeasurementsListUseCase:
    """
    Usecase class that contains the logic to list all the measurements of the anemometers with a pagination
    """

    def __init__(self, request_data: dict, serializer: Optional[Serializer] = None):
        self.request_data = request_data
        self.serializer = serializer

    def execute(self) -> Response:

        # Check if the anemometer exists
        anemometer = get_object_or_404(Anemometer, pk=self.request_data.get('anemometer'))

        # Get the limit and offset from the request query params
        limit = self.request_data.get('limit', None)
        offset = self.request_data.get('offset', None)

        # Validate the limit and offset
        if limit and offset:
            limit, offset = validate_limit_and_offset(limit, offset)
        else:
            limit = 20
            offset = 0
        
        # Get the measurements with pagination for this anemometer
        measurements = Anemometer.get_all_measurements_for_anemometer(self.request_data.get('anemometer'), limit, offset)
        
        # Create the response
        response: dict = {
            "measurements": list(measurements.values())
        }
        # Return the response
        return Response(response, status=status.HTTP_200_OK)







