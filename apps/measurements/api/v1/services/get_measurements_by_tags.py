# Standard imports
from typing import Optional

# Django imports
from django.http import HttpRequest
from django.contrib.auth import get_user_model, authenticate

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

# Serializers
from apps.anemometers.api.v1.serializers import AnemometerMeasurementSerializer

# Models
from apps.measurements.models.measurement import Measurement


class MeasurementsByTagsUseCase:
    """
    Usecase class that contains the logic to retrieve anemometer measurements filterd by a set of tags
    """

    def __init__(self, request_data: dict, serializer: Optional[Serializer] = None):
        self.request_data = request_data
        self.serializer = serializer

    def execute(self) -> Response:

        # Get the tags from the request
        tags = self.request_data.get('tags', [])
        print(tags)

        if not tags:
            return Response({"error": "No tags provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the measurements filtered by the tags, response i
        measurements: list[dict] = Measurement.list_anemometer_measurements_by_anemometer_tags(tags)

        # Create the response
        response = {
            "measurements": measurements
        }

        # Return the response
        return Response(response, status=status.HTTP_200_OK)



