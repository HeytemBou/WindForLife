# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
from random import randint
import random

# Model imports
from apps.anemometers.models.anemometer import Anemometer

faker_g = fk(['en_US', 'fr_FR'])
faker_g.seed_instance(randint(1, 100000))


def generate_fake_tags():
    tags = ['tag1', 'tag2', 'tag3']
    return random.sample(tags, random.randint(1, 3))


class AnemometerFactory(DjangoModelFactory):
    """
    Factory for Anemometer model
    """

    class Meta:
        model = Anemometer

    name = Faker('name')
    tags = Faker('tags')
    measurement_unit = Faker('measurement_unit')
    location = Faker('location')
