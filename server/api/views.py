from rest_framework import generics
from django.shortcuts import render

from . import models
from . import serializers
from .tasks import test_that_it_works


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


def celery_test(request):
    output = test_that_it_works.delay()
    res = output.get()
    return render(request, 'celery_test.html', {'output': res})
