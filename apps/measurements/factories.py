# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
from random import randint
import random

# Model imports
from apps.measurements.models.measurement import Measurement


faker_g = fk(['en_US', 'fr_FR'])
faker_g.seed_instance(randint(1, 100000))



class MeasurementFactory(DjangoModelFactory):
    """
    Factory for Measurement model
    """

    class Meta:
        model = Measurement

    name = Faker('name')
    wind_speed = Faker('random_int', min=0, max=100)
    timestamp = Faker('date_time_this_month')
    unit = 'knots'
