# Standard imports
from typing import Optional
from datetime import datetime, timezone, timedelta

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


class MeasurementsStatsUseCase:
    """
    Usecase class that contains the logic to retrieve stats about the measurements of the anemometers
    """

    def __init__(self, request: HttpRequest, serializer: Optional[Serializer] = None):
        self.request = request
        self.serializer = serializer

    def execute(self) -> Response:
        """
        Method that executes the usecase and returns the response
        """

        date: datetime = self.request.data.get('date', None)

        # Check if the date is provided and is in the correct format and get the week start and end dates
        if date is None:
            date = datetime.now(timezone.utc)
            week_start = date - timedelta(days=date.weekday())
            week_end = week_start + timedelta(days=6)
        else:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
                week_start = date - timedelta(days=date.weekday())
                week_end = week_start + timedelta(days=6)
            except ValueError:
                return Response({"error": "Invalid date format. Use the format 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the daily average speed of each anemometer
        daily_avg_speed = Measurement.daily_average_wind_speed_for_each_anemometer(date)

        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)

        weekly_avg_speed = Measurement.weekly_average_wind_speed_for_each_anemometer(week_start, week_end)

        # Convert the queryset to a list of dictionaries
        daily_avg_speed = [entry for entry in daily_avg_speed]
        weekly_avg_speed = [entry for entry in weekly_avg_speed]

        # Create the response
        response = {
            "date used": date,
            "daily_avg_speed": daily_avg_speed,
            "weekly_avg_speed": weekly_avg_speed
        }

        # Return the response
        return Response(response, status=status.HTTP_200_OK)







