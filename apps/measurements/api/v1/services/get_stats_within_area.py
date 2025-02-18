# Standard imports
from typing import Optional
from datetime import datetime, timezone

# Django imports
from django.http import HttpRequest

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

# Models
from apps.anemometers.models.anemometer import Anemometer
from apps.measurements.models.measurement import Measurement

# Validators
from apps.anemometers.api.v1.validators import validate_latitude, validate_longitude, validate_radius

# Utils
from utils.geo.haversine_distance import compute_haversine_distance


class StatsWithinAreaUseCase:
    """
    Usecase class that contains the logic to get the statistics of measurements within a given area defined by a central point and a radius
    """

    def __init__(self, request_data: dict, serializer: Optional[Serializer] = None):
        self.request_data = request_data
        self.serializer = serializer

    def execute(self) -> Response:

        # Get the latitude and longitude from the request query params, as well as the radius
        latitude: Optional[float] = self.request_data.get('latitude', None)
        longitude: Optional[float] = self.request_data.get('longitude', None)
        radius: Optional[float] = self.request_data.get('radius', None)
        date: Optional[str] = self.request_data.get('date', None)

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format. Use the format 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            date = datetime.now(timezone.utc)   

        if not latitude or not longitude or not radius:
            return Response({"error": "Latitude, longitude and radius are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the latitude, longitude and radius
        if not validate_latitude(latitude) or not validate_longitude(longitude) or not validate_radius(radius):
            return Response({"error": "Invalid latitude, longitude or radius"}, status=status.HTTP_400_BAD_REQUEST)

        # Get all anemometers
        anemometers = Anemometer.objects.all()

        anemometers_in_area: list[Anemometer] = []

        # For each anemometer we compute the distance between it and the central point
        for anemometer in anemometers:
            distance = compute_haversine_distance(anemometer.latitude, anemometer.longitude, latitude, longitude)
            # If the distance is less than the radius, we add the anemometer to the list
            if distance <= radius:
                anemometers_in_area.append(anemometer)

        # Now retrieve wind speed across all anemometers in the area at the given date
        measurements_in_area = Measurement.get_measurements_by_anemometers_at_given_date(anemometers_in_area, date)

        # Compute the average wind speed, min wind speed and max wind speed
        average_wind_speed = sum([measurement.wind_speed for measurement in measurements_in_area]) / len(measurements_in_area) if measurements_in_area else 0
        min_wind_speed = min([measurement.wind_speed for measurement in measurements_in_area]) if measurements_in_area else 0
        max_wind_speed = max([measurement.wind_speed for measurement in measurements_in_area]) if measurements_in_area else 0

        return Response({
            "average_wind_speed": average_wind_speed,
            "min_wind_speed": min_wind_speed,
            "max_wind_speed": max_wind_speed
        }, status=status.HTTP_200_OK)



