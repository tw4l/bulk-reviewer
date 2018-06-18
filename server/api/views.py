from rest_framework import generics
from django.shortcuts import render

from . import models
from . import serializers
from .tasks import run_bulk_extractor


class ListTransfer(generics.ListAPIView):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer


class DetailTransfer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer


class ListFile(generics.ListAPIView):
    queryset = models.File.objects.filter(be_session=pk)
    serializer_class = serializers.FileSerializer


class DetailFile(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer


class ListFeature(generics.ListAPIView):
    queryset = models.Feature.objects.filter(source_file=pk)
    serializer_class = serializers.FeatureSerializer


class DetailFeature(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class ListBEConfig(generics.ListAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class DetailBEConfig(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class ListBESession(generics.ListAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


class DetailBESession(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


def bulk_extractor(request, pk):
    output = run_bulk_extractor.delay(pk)
    res = output.get()
    return render(request, 'bulk_extractor_test.html', {'output': res})
