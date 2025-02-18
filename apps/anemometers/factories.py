# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from factory import Faker, post_generation
from faker import Faker as fk
from random import randint
import random

# Model imports
from apps.anemometers.models.anemometer import Anemometer
from apps.anemometers.models.anemometer_tag import AnemometerTag

faker_g = fk(['en_US', 'fr_FR'])
faker_g.seed_instance(randint(1, 100000))



class AnemometerTagFactory(DjangoModelFactory):
    """
    Factory for AnemometerTag model
    """

    class Meta:
        model = AnemometerTag

    name = Faker('name')

class AnemometerFactory(DjangoModelFactory):
    """
    Factory for Anemometer model
    """

    class Meta:
        model = Anemometer

    name = Faker('name')
    longitude = Faker('longitude')
    latitude = Faker('latitude')
    altitude = Faker('altitude')

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Create a default set of tags
            for _ in range(3):  # Adjust the range for the number of tags you want to create
                tag = AnemometerTagFactory()
                self.tags.add(tag)
    
