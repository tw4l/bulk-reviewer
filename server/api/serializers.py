from rest_framework import serializers
from . import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    source_filepath = serializers.CharField(source='source_file.filepath')

    class Meta:
        model = models.Feature
        fields = ('uuid', 'feature_file', 'forensic_path', 'offset',
                  'feature', 'context', 'note', 'cleared', 'source_file',
                  'source_filepath')


class NamedEntitySerializer(serializers.ModelSerializer):
    source_filepath = serializers.CharField(source='source_file.filepath')

    class Meta:
        model = models.NamedEntity
        fields = ('uuid', 'text', 'label', 'source_file',
                  'source_filepath')


class BEConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BEConfig
        fields = '__all__'


class BESessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BESession
        fields = '__all__'


class RedactedSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RedactedSet
        fields = '__all__'
