# Standard imports
from datetime import timezone

# rest framework imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Local imports
from apps.anemometers.api.v1.services.submit_anemometer_measurements_usecase import AnemometerMeasurementsUseCase
from apps.anemometers.models.anemometer import Anemometer

# Serializers
from apps.anemometers.api.v1.serializers import AnemometerCreateSerializer

# Utils imports
from utils.security.jwt_authentication import JWTAuthentication

# Usecases
from apps.anemometers.api.v1.services.list_anemometer_measurements_usecase import MeasurementsListUseCase
from apps.anemometers.api.v1.services.submit_anemometer_measurements_usecase import AnemometerMeasurementsUseCase


class AnemometerViewSet(viewsets.ModelViewSet):
    """Viewset for managing anemometers and their measurements"""

    queryset = Anemometer.objects.all()
    serializer_class = AnemometerCreateSerializer
    authentication_classes = [JWTAuthentication]

    # Custom action url path for submitting measurements to a specific anemometer at a specific time
    @action(methods=['post'], url_path="(?P<id>[^/.]+)/measurements", detail=False, authentication_classes=[JWTAuthentication])
    def submit_measurement(self, request, id: str):
        """
        API to submit a measurement to an anemometer
        """
        # Create a mutable copy of request.data
        data = request.data.copy()
        # Add the anemometer id to the request data
        data['anemometer'] = id
        
        # Instantiate the usecase
        usecase = AnemometerMeasurementsUseCase(data)
        # Execute the usecase and get the response
        response: Response = usecase.execute()
        
        return response
    
    # Custom action url path for getting the measurements of a specific anemometer with pagination
    @action(methods=['get'], url_path="(?P<id>[^/.]+)/measurements", detail=False, authentication_classes=[JWTAuthentication])
    def get_measurements(self, request, id: str):
        """
        API to get the measurements of an anemometer
        """
        # Create a mutable copy of request.data
        data = request.data.copy()
        # Add the anemometer id to the request data
        data['anemometer'] = id

        # Get the limit and offset from the request query params
        limit = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', None)
        # Add the limit and offset to the request data
        data['limit'] = limit
        data['offset'] = offset

        # Instantiate the usecase
        usecase = MeasurementsListUseCase(data)
        # Execute the usecase and get the response
        response: Response = usecase.execute()
        
        return response

