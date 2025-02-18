# Standard imports
from uuid import uuid4

# Django imports
from django.db import models

# Local imports
from apps.accounts.models.time_stamped_model import TimeStampedModel


class Anemometer(TimeStampedModel):
    """
    Model for Anemometer
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField('AnemometerTag', related_name='anemometer_tags')
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()

    class Meta:
        db_table = 'anemometers'
    
    def __str__(self):
        return self.name + " - " + str(self.id)

    @classmethod
    def delete_anemometer_by_id(self, anemometer_id):
        Anemometer.objects.filter(id=anemometer_id).delete()

    @classmethod
    def get_anemometer_by_tags(self, tags):
        """
        List all anemometers that match at least one of the tags
        """
        return Anemometer.objects.filter(tags__name__in=tags).distinct()
    
    @classmethod
    def get_all_measurements_for_anemometer(self, anemometer_id: str, limit: int, offset: int):
        """
        Get all measurements for a specific anemometer with pagination
        """
        return Anemometer.objects.get(id=anemometer_id).measurements.all()[offset:limit+offset]
