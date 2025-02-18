from uuid import uuid4

# Local imports
from django.contrib.gis.db import models
from apps.accounts.models import TimeStampedModel


class Anemometer(TimeStampedModel):
    """
    Model for Anemometer
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField('AnemometerTag', related_name='anemometer_tags')
    measurement_unit = models.CharField(max_length=10, default="Knots")
    location = models.PointField()

    class Meta:
        db_table = 'anemometers'

    def __str__(self):
        return self.name

    @classmethod
    def delete_anemometer_by_id(self, anemometer_id):
        Anemometer.objects.filter(id=anemometer_id).delete()

    @classmethod
    def get_anemometer_by_tags(self, tags):
        """
        List all anemometers that match at least one of the tags
        """
        return Anemometer.objects.filter(tags__name__in=tags).distinct()
