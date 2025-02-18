
# Factory imports
from apps.accounts.factories import AccountFactory
from apps.anemometers.factories import AnemometerFactory, AnemometerTagFactory
from apps.measurements.factories import MeasurementFactory

# factory boy imports
import factory
from factory import Faker

def generate_fake_db_data(data_scale: int=100):
     # Track the number of created entries
    account_count = 5
    anemometer_count = 5
    tags_count = 10

    # Create dynamic data
    for i in range(data_scale):
        # Create Accounts
        AccountFactory.create_batch(account_count)

        # Create Anemometers and associated tags
        tags = AnemometerTagFactory.create_batch(tags_count)
        AnemometerFactory.create_batch(anemometer_count, tags=tags)

        # Create Measurements
        MeasurementFactory.create_batch(100)