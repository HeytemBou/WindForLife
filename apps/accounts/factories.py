import json
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
from random import randint

# Model imports
from apps.accounts.models.account import Account

fake = fk()
# Create faker object with 3 languages as providers : english, french and arabic
faker_g = fk(['en_US', 'fr_FR'])
faker_g.seed_instance(randint(1, 1000000))

emails_set = set()


def generate_unique_email():
    email = faker_g.email()
    while email in emails_set:
        email = faker_g.email()
    emails_set.add(email)
    return email


################### Account Factory ###################
class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    email = factory.LazyFunction(generate_unique_email)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_active = Faker('boolean', chance_of_getting_true=90)
    is_staff = Faker('boolean', chance_of_getting_true=0)
    is_superuser = Faker('boolean', chance_of_getting_true=0)
    is_admin = Faker('boolean', chance_of_getting_true=0)

    @factory.post_generation
    def log_creation(self, create, extracted, **kwargs):
        if create:
            print(f"Created Account for account ID {self.id}")
