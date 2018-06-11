from rest_framework import generics

from . import models
from . import serializers


class ListTransfer(generics.ListCreateAPIView):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer


class DetailTransfer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer


class ListFile(generics.ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer


class DetailFile(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer


class ListFeature(generics.ListCreateAPIView):
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class DetailFeature(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class ListBEConfig(generics.ListCreateAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class DetailBEConfig(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class ListBESession(generics.ListCreateAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


class DetailBESession(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer
