# rest framework imports
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

from apps.anemometers.api.v1.viewsets import AnemometerViewSet

############################## Router for User Management API ##############################

router = DefaultRouter(trailing_slash=False)
router.register('v1/measurements', AnemometerViewSet, basename='measurement')

urlpatterns = [
    path('', include(router.urls)),
]