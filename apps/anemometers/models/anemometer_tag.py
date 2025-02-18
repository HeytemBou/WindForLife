# Standard imports
from uuid import uuid4

# Local imports
from django.contrib.gis.db import models
from apps.accounts.models import TimeStampedModel


class AnemometerTag(TimeStampedModel):
    """
    Model for Anemometer Tags
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'anemometer_tags'

    def __str__(self):
        return self.name
