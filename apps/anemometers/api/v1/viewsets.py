# Standard imports
from datetime import timezone

# rest framework imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Local imports
from apps.anemometers.models import Anemometer, AnemometerTag
from apps.measurements.models import Measurement

# Serializers
from apps.anemometers.api.v1.serializers import AnemometerCreateSerializer

# Utils imports
from utils.security.jwt_authentication import JWTAuthentication

# Usecases
from apps.anemometers.api.v1.services.submit_anemometer_measurements_usecase import AnemometerMeasurementsUseCase


class AnemometerViewSet(viewsets.ModelViewSet):
    """Viewset for managing anemometers and their measurements"""

    queryset = Anemometer.objects.all()
    serializer_class = AnemometerCreateSerializer
    authentication_classes = [JWTAuthentication]

    # Custom action url path for submitting measurements to a specific anemometer
    @action(methods=['post'], url_path="(?P<id>[^/.]+)/measurements", detail=False, authentication_classes=[JWTAuthentication])
    def submit_measurement(self, request, id: str):
        """
        API to submit a measurement to an anemometer
        """
        # Add the anemometer id to the request data
        request.data['anemometer'] = id
        # Instantiate the usecase
        usecase = AnemometerMeasurementsUseCase(request)
        # Execute the usecase and get the response
        response: Response = usecase.execute()
        return response

