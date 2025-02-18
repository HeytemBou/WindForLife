# Standard imports
from datetime import timezone, datetime

# rest framework imports
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Usecase imports
from apps.measurements.api.v1.services.measurements_stats_usecase import MeasurementsStatsUseCase
from apps.measurements.api.v1.services.get_measurements_by_tags import MeasurementsByTagsUseCase

# Local imports
from apps.measurements.models import Measurement
from apps.anemometers.models import Anemometer

# Utils imports
from utils.security.jwt_authentication import JWTAuthentication


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing measurements and their statistics
    """

    queryset = Measurement.objects.all()
    authentication_classes = [JWTAuthentication]

    # Custom action url path for getting the daily and weekly mean wind speed of each anemometer
    @action(methods=['get'], url_path="wind-speed-stats", detail=False, authentication_classes=[JWTAuthentication])
    def wind_speed_stats(self, request):
        """
        API to get the daily and weekly mean wind speed of each anemometer
        """
        # First get the date from the request query params if it exists
        date = request.query_params.get('date', None)
        # Check if the date is provided and is in the correct format
        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
                request.data['date'] = date
            except ValueError:
                return Response({"error": "Invalid date format. Use the format 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)

        # Instantiate the usecase
        usecase = MeasurementsStatsUseCase(request)
        # Execute the usecase and get the response
        response: Response = usecase.execute()
        return response

    # Custom action endpoint to filter anemometer measurements given a set of tags
    @action(methods=['get'], url_path="filter-by-tags", detail=False, authentication_classes=[JWTAuthentication])
    def filter_by_tags(self, request):
        """
        API to filter anemometer measurements by a set of tags
        """
        # Get the tags from the request query params
        tags: list[str] = request.query_params.get('tags', None)
        # Inject the tags into the request data
        request.data['tags'] = tags

        # instantiate the usecase
        usecase = MeasurementsByTagsUseCase(request)
        # Execute the usecase and get the response
        response: Response = usecase.execute()
        return response

    # Custom action endpoint to