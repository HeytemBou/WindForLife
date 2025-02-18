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
from apps.anemometers.models import Anemometer, AnemometerTag
from apps.measurements.models import Measurement


class MeasurementsStatsUseCase:
    """
    Usecase class that contains the logic to create an anemometer
    """

    def __init__(self, request: HttpRequest, serializer: Optional[Serializer] = None):
        self.request = request
        self.serializer = serializer

    def execute(self) -> Response:

        # Get the daily average speed of each anemometer
        daily_avg_speed = Measurement.daily_average_wind_speed_for_each_anemometer(self.request.data['date'])
        weekly_avg_speed = Measurement.weekly_average_wind_speed_for_each_anemometer(self.request.data['date'])

        # Convert the queryset to a list of dictionaries
        daily_avg_speed = list(daily_avg_speed.values())
        weekly_avg_speed = list(weekly_avg_speed.values())

        # Create the response
        response = {
            "daily_avg_speed": daily_avg_speed,
            "weekly_avg_speed": weekly_avg_speed
        }

        # Return the response
        return Response(response, status=status.HTTP_200_OK)







