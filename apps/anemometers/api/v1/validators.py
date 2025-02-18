# Rest framework imports
from rest_framework import serializers


def validate_longitude(value: float):
    """
    Validate that the value is a valid longitude
    """
    if not -180 <= value <= 180:
        raise serializers.ValidationError("LONGITUDE_OUT_OF_RANGE")
    return True

def validate_latitude(value: float):
    """
    Validate that the value is a valid latitude
    """
    if not -90 <= value <= 90:
        raise serializers.ValidationError("LATITUDE_OUT_OF_RANGE")
    return True


def validate_altitude(value: float) -> bool:
    """
    Validate that the value is a valid elevation
    """
    if value < 0:
        raise serializers.ValidationError("ELEVATION_NEGATIVE")
    return True


def validate_radius(value: str) -> bool:
    """
    Validate that the value is a valid radius
    """
    if value < 0:
        raise serializers.ValidationError("RADIUS_NEGATIVE")
    return True


def validate_anemometer_name(value: str):
    """
    Validate that the value is a valid anemometer name
    """
    if len(value) < 3:
        raise serializers.ValidationError("ANEMOMETER_NAME_TOO_SHORT")
    if len(value) > 50:
        raise serializers.ValidationError("ANEMOMETER_NAME_TOO_LONG")


def validate_anemometer_tags(value: str):
    """
    Tags should be a list of strings separated by commas
    """
    tags = value.split(',')
    for tag in tags:
        if len(tag) < 3:
            raise serializers.ValidationError("TAG_NAME_TOO_SHORT")
        if len(tag) > 50:
            raise serializers.ValidationError("TAG_NAME_TOO_LONG")
    return tags


def validate_limit_and_offset(limit: str, offset: str) -> tuple[int, int]:
    """
    Validate the limit and offset query parameters, both should be integers and positive
    """
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 0 or limit > 100:
                raise serializers.ValidationError("LIMIT_NEGATIVE")
        except ValueError:
            raise serializers.ValidationError("LIMIT_NOT_INTEGER")

    if offset is not None:
        try:
            offset = int(offset)
            if offset < 0:
                raise serializers.ValidationError("OFFSET_NEGATIVE")
        except ValueError:
            raise serializers.ValidationError("OFFSET_NOT_INTEGER")
    return limit, offset