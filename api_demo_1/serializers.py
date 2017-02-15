from rest_framework import serializers
from models import *

class GeospaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geospace
        fields = ('latitude', 'longitude')

class MorchaSerializer(serializers.ModelSerializer):
    geospace = GeospaceSerializer()
    class Meta:
        model = Morcha
        fields = ('name', 'geospace', 'uuid')

class PostSerializer(serializers.ModelSerializer):
    morchas = MorchaSerializer(many=True, read_only = True)
    geospace = GeospaceSerializer()
    class Meta:
        model = Post
        fields = ('name', 'geospace', 'uuid', 'morchas',)

class IntrusionSerializer(serializers.ModelSerializer):
    #morcha = MorchaSerializer()
    class Meta:
        model = Intrusion
        fields = ('detected_datetime', 'verified_datetime', 'neutralized_datetime',
                  'non_human_intrusion_datetime', 'duration')

class ReportDataSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    engagement_time = serializers.FloatField()

class WeekReportSerializer(serializers.Serializer):
    day = serializers.DateField()

class LongestIntrusionSerializer(serializers.ModelSerializer):
    morcha = MorchaSerializer()
    class Meta:
        model = Intrusion
        fields = ('detected_datetime', 'verified_datetime', 'neutralized_datetime',
                  'non_human_intrusion_datetime', 'duration', 'morcha')

class MorchaNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Morcha
        fields = ('name', 'uuid')

