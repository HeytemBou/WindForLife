# Django rest framework
from django.shortcuts import get_object_or_404

# local imports
from apps.anemometers.models import Anemometer, AnemometerTag
from apps.measurements.models import Measurement

# rest framework imports
from rest_framework import serializers

# Validators
from apps.anemometers.api.v1.validators import validate_longitude, validate_latitude, validate_elevation, validate_anemometer_name, validate_anemometer_tags, validate_limit, validate_offset


class GenericAnemometerSerializer(serializers.ModelSerializer):
    """
    Generic serializer class for anemometers
    """
    class Meta:
        model = Anemometer
        fields = ['id', 'name', 'tags', 'measurement_unit', 'latitude', 'longitude', 'elevation']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'validators': [validate_anemometer_name]},
            'tags': {'validators': [validate_anemometer_tags]},
            'latitude': {'validators': [validate_latitude]},
            'longitude': {'validators': [validate_longitude]},
            'elevation': {'validators': [validate_elevation]}
        }
    
    def to_representation(self, instance):
        """
        Convert the model instance to a dictionary
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'tags': instance.tags,
            'measurement_unit': instance.measurement_unit,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'elevation': instance.elevation
        }


class AnemometerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating anemometers
    """
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )
    class Meta:
        model = Anemometer
        fields = ['name', 'tags', 'measurement_unit', 'latitude', 'longitude', 'elevation']
        extra_kwargs = {
            'name': {'validators': [validate_anemometer_name]},
            'tags': {'validators': [validate_anemometer_tags]},
            'latitude': {'validators': [validate_latitude]},
            'longitude': {'validators': [validate_longitude]},
            'elevation': {'validators': [validate_elevation]}
        }

    def create(self, validated_data):
        """
        Create and return a new `Anemometer` instance, given the validated data.
        The tags should be handled differently, as they are a list of strings separated by commas.
        """
        tags = validated_data.pop('tags')
        anemometer = Anemometer.objects.create(**validated_data)
        if tags:
            for tag_name in tags:
                tag, created = AnemometerTag.objects.get_or_create(name=tag_name)
                print(created)
                print(tag)
                anemometer.tags.add(tag)
        return anemometer

class AnemometerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer class for updating anemometers
    """
    
    class Meta:
        model = Anemometer
        fields = ['name', 'tags', 'measurement_unit', 'latitude', 'longitude', 'elevation']
        extra_kwargs = {
            'name': {'validators': [validate_anemometer_name]},
            'tags': {'validators': [validate_anemometer_tags]},
            'latitude': {'validators': [validate_latitude]},
            'longitude': {'validators': [validate_longitude]},
            'elevation': {'validators': [validate_elevation]}
        }

    def update(self, instance, validated_data):
        """
        Update and return an existing `Anemometer` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.measurement_unit = validated_data.get('measurement_unit', instance.measurement_unit)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.elevation = validated_data.get('elevation', instance.elevation)
        tags = validated_data.get('tags').split(',')
        anemometer = instance.save()
        if tags:
            # Remove all tags related to this anemometer
            instance.tags.clear()
            # Add the new tags
            for tag_name in tags:
                tag, created = AnemometerTag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return anemometer
                

        

class AnemometerListSerializer(serializers.ModelSerializer):
    """
    Serializer class for listing anemometers
    """    
    class Meta:
        model = Anemometer
        fields = ['id', 'name', 'tags', 'latitude', 'longitude', 'elevation']
    
    def to_representation(self, instance):
        """
        Convert the model instance to a dictionary
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'tags': instance.tags,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'elevation': instance.elevation
        }

class AnemometerDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer class for deleting anemometers
    """
    id = serializers.UUIDField()
    class Meta:
        model = Anemometer
        fields = ['id']
    
    def delete(self, validated_data):
        """
        Delete the `Anemometer` instance, given the validated data.
        """
        print(validated_data)
        Anemometer.delete_anemometer_by_id(validated_data.get('id'))
        return None


class AnemometerMeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating anemometer measurements for a given anemometer
    """
    class Meta:
        model = Measurement
        fields = ['id', 'anemometer', 'wind_speed', 'timestamp']
        read_only_fields = ['id']
        extra_kwargs = {
            'anemometer': {'required': True},
            'wind_speed': {'required': True},
            'timestamp': {'required': True}
        }
    
    def create(self, validated_data):
        """
        Create and return a new `Measurement` instance, given the validated data.
        """
        # First check if the anemometer exists, if it doesn't, raise a 404 error
        anemometer = get_object_or_404(Anemometer, id=validated_data.get('anemometer'))
        validated_data['anemometer'] = anemometer
        
        return Measurement.objects.create(**validated_data)
    
    def to_representation(self, instance):
        """
        Convert the model instance to a dictionary
        """
        return {
            'id': instance.id,
            'anemometer': instance.anemometer,
            'wind_speed': instance.wind_speed,
            'unit': instance.unit,
            'timestamp': instance.timestamp
        }
    
   