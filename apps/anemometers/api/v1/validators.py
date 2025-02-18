# Rest framework imports
from rest_framework import serializers


def validate_longitude(value):
    """
    Validate that the value is a valid longitude
    """
    if not -180 <= value <= 180:
        raise serializers.ValidationError("LONGITUDE_OUT_OF_RANGE")


def validate_latitude(value):
    """
    Validate that the value is a valid latitude
    """
    if not -90 <= value <= 90:
        raise serializers.ValidationError("LATITUDE_OUT_OF_RANGE")


def validate_elevation(value):
    """
    Validate that the value is a valid elevation
    """
    if value < 0:
        raise serializers.ValidationError("ELEVATION_NEGATIVE")


def validate_radius(value):
    """
    Validate that the value is a valid radius
    """
    if value < 0:
        raise serializers.ValidationError("RADIUS_NEGATIVE")


def validate_anemometer_name(value):
    """
    Validate that the value is a valid anemometer name
    """
    if len(value) < 3:
        raise serializers.ValidationError("ANEMOMETER_NAME_TOO_SHORT")
    if len(value) > 50:
        raise serializers.ValidationError("ANEMOMETER_NAME_TOO_LONG")


def validate_anemometer_tags(value):
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


def validate_limit(value):
    """
    Validate that the value is a valid limite
    """
    if value < 0 and value > 20:
        raise serializers.ValidationError("LIMITE_OUT_OF_RANGE")


def validate_offset(value):
    """
    Validate that the value is a valid offset
    """
    if value < 0:
        raise serializers.ValidationError("OFFSET_OUT_OF_RANGE")
