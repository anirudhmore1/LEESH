from django.contrib.auth.models import User, Group
from .models import GPSData,ClueMedia,WaypointsData,GPShistoricalData
from rest_framework import serializers

class GPSDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GPSData
        fields = ('deviceid', 'taskid', 'gpsdata')

class WaypointsDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WaypointsData
        fields = ('deviceid', 'taskid','waypointsdata')

class GPShistoricalDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GPShistoricalData
        fields = ('deviceid', 'taskid','gpshistoricaldata')

class ClueMediaSerializer(serializers.HyperlinkedModelSerializer):
    #photo = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)
    #doc = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = ClueMedia
        fields = ('id', 'name', 'longitude', 'latitude', 'photo', 'description')
