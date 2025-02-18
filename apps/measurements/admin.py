# Django imports
from django.contrib import admin

# Local imports
from apps.measurements.models.measurement import Measurement


admin.site.register(Measurement)