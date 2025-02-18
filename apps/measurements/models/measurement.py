# Standard imports
from typing import Optional
from datetime import datetime, timezone, timedelta

# Django imports
from django.db import models

# Local imports
from apps.accounts.models.time_stamped_model import TimeStampedModel


class Measurement(TimeStampedModel):
    """
    Model class for storing wind speed readings from anemometers
    """
    anemometer = models.ForeignKey('anemometers.Anemometer', on_delete=models.CASCADE, related_name='measurements')
    wind_speed = models.FloatField()
    unit = models.CharField(max_length=10, default='knots')
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.anemometer.name} - {self.wind_speed} - {self.unit}'

    class Meta:
        db_table = 'measurements'

    @classmethod
    def daily_average_wind_speed_for_each_anemometer(cls, date: Optional[datetime] = None):
        """
        Returns the average wind speed for each anemometer on a given day, if no date is provided, it will return the average wind speed for the current day
        """
        if date is None:
            date = datetime.now(timezone.utc)
        return Measurement.objects.filter(timestamp__date=date).values('anemometer__name').annotate(models.Avg('wind_speed'))

    @classmethod
    def weekly_average_wind_speed_for_each_anemometer(cls, date: Optional[datetime] = None):
        """
        Returns the average wind speed for each anemometer on a given week, if no date is provided, it will return the average wind speed for the current week
        """
        if date is None:
            date = datetime.now(timezone.utc)
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)
        return Measurement.objects.filter(timestamp__date__range=[week_start, week_end]).values('anemometer__name').annotate(models.Avg('wind_speed'))

    @classmethod
    def list_anemometer_measurements_by_anemometer_tags(cls, tags: Optional[str]) -> list[dict]:
        """
        Filter and group anemometer measurements by tags
        """
        result = Measurement.objects.filter(anemometer__tags__name__in=tags).values('anemometer__name').annotate(models.Avg('wind_speed'))
        # convert the queryset to a list
        result = list(result)

        return result

    @classmethod
    def get_measurements_by_anemometers_at_given_date(cls, anemometers: list[anemometer], date: Optional[datetime] = None):
        """
        Returns a list of measurements for a list of anemometers at a given date
        """
        if date is None:
            date = datetime.now(timezone.utc)
        return Measurement.objects.filter(anemometer__in=anemometers, timestamp__date=date)
