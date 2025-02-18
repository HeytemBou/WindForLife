# rest framework imports
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

from apps.measurements.api.v1.viewsets import MeasurementViewSet

############################## Router for Measurements app ##############################

router = DefaultRouter(trailing_slash=False)
router.register('v1/measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('', include(router.urls)),
]