from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from . import models
from . import serializers


class ListFile(generics.ListAPIView):
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        """
        This view should return a list of all the files for
        the session as determined by the UUID portion of the URL.
        """
        session = self.kwargs['pk']
        return models.File.objects.filter(be_session=session)


class DetailFile(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer


class ListFeature(generics.ListAPIView):
    serializer_class = serializers.FeatureSerializer

    def get_queryset(self):
        """
        This view should return a list of all the features for
        the file as determined by the UUID portion of the URL.
        """
        source_file = self.kwargs['pk']
        return models.Feature.objects.filter(source_file=source_file)


class UpdateFeatureList(APIView):
    parser_classes = (JSONParser,)

    def patch(self, request, format=None):
        feature_list = request.data.feature_list
        cleared_status = request.data.cleared

        for feature in feature_list:
            instance = models.Feature.get(uuid=feature)
            instance.cleared = cleared_status
            instance.save()
            data.append(instance)

        return Response({'status': 'SUCCESS'})


class ListFeatureBySession(generics.ListAPIView):
    serializer_class = serializers.FeatureSerializer

    def get_queryset(self):
        """
        This view should return a list of all the features for
        the session as determined by the UUID portion of the URL.
        """
        session = self.kwargs['pk']
        return models.Feature.objects.filter(source_file__be_session=session)


class DetailFeature(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class CreateBEConfig(generics.CreateAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class ListBEConfig(generics.ListAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class DetailBEConfig(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BEConfig.objects.all()
    serializer_class = serializers.BEConfigSerializer


class CreateBESession(generics.CreateAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


class ListBESession(generics.ListAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


class DetailBESession(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BESession.objects.all()
    serializer_class = serializers.BESessionSerializer


class CreateRedactedSet(generics.CreateAPIView):
    queryset = models.RedactedSet.objects.all()
    serializer_class = serializers.RedactedSetSerializer


class ListRedactedSet(generics.ListAPIView):
    queryset = models.RedactedSet.objects.all()
    serializer_class = serializers.RedactedSetSerializer


class DetailRedactedSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.RedactedSet.objects.all()
    serializer_class = serializers.RedactedSetSerializer


class ListRedactedSetBySession(generics.ListAPIView):
    serializer_class = serializers.RedactedSetSerializer

    def get_queryset(self):
        """
        This view should return a list of all the redacted sets for
        the session as determined by the UUID portion of the URL.
        """
        be_session = self.kwargs['pk']
        return models.RedactedSet.objects.filter(be_session=be_session)
