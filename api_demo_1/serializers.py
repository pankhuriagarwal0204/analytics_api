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

class PostMorchaSerializer(serializers.ModelSerializer):
    morchas = MorchaSerializer(many=True, read_only = True)
    geospace = GeospaceSerializer()
    class Meta:
        model = Post
        fields = ('name', 'geospace', 'uuid', 'morchas')

class PostNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'uuid')

class BattalionSerializer(serializers.ModelSerializer):
    geospace = GeospaceSerializer()
    posts = PostNameSerializer(many=True)

    class Meta:
        model = Morcha
        fields = ('name', 'geospace', 'uuid', 'posts')

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

class MorchaNameSerializer(serializers.ModelSerializer):
    post = PostNameSerializer()
    class Meta:
        model = Morcha
        fields = ('name', 'uuid', 'post')

class LongestIntrusionSerializer(serializers.ModelSerializer):
    morcha = MorchaNameSerializer()
    class Meta:
        model = Intrusion
        fields = ('detected_datetime', 'verified_datetime', 'neutralized_datetime',
                  'non_human_intrusion_datetime', 'duration', 'morcha', 'morcha')



