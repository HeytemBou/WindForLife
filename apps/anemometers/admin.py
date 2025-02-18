# Django imports
from django.contrib import admin

# Local imports
from .models.anemometer import Anemometer
from .models.anemometer_tag import AnemometerTag


class AnemometerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', 'latitude', 'longitude', 'elevation')


admin.site.register(Anemometer, AnemometerAdmin)
admin.site.register(AnemometerTag)
