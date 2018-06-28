from rest_framework import serializers
from . import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = '__all__'


class BEConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BEConfig
        fields = '__all__'


class BESessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BESession
        fields = '__all__'
