from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

import os
import zipfile
from io import BytesIO

from . import models
from . import serializers
from . import tasks


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
        """
        This view should update the 'cleared' status using
        the supplied value for Features with supplied UUIDs
        """
        feature_list = request.data['feature_list']
        cleared_status = request.data['cleared']

        tasks.update_features.delay(feature_list, cleared_status)
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


def download_csv_reports(request, pk):
    # Get session
    be_session = get_object_or_404(models.BESession, pk=pk)
    # Generate reports and wait for result
    output = tasks.create_csv_reports.delay(str(be_session.uuid))
    output.get()
    # Calculate filenames to include in zip
    dismissed_file = be_session.name + '_dismissed.csv'
    dismissed_fpath = os.path.join(settings.MEDIA_ROOT,
                                   'csv_reports',
                                   str(pk),
                                   dismissed_file)
    redact_file = be_session.name + '_to_redact.csv'
    redact_fpath = os.path.join(settings.MEDIA_ROOT,
                                'csv_reports',
                                str(pk),
                                redact_file)
    filenames = [dismissed_fpath, redact_fpath]
    # Zip folder and filename
    zip_subdir = str(pk)
    zip_filename = "{}.zip".format(zip_subdir)
    # Open BytesIO to grab in-memory ZIP contents
    zip_io = BytesIO()
    # Write zip file contents
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            # Add file, at correct path
            zf.write(fpath, zip_path)
    # Grab zip file from in-memory, make response with correct headers
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename={}'.format(zip_filename)
    response['Content-Length'] = zip_io.tell()
    # Return response
    return response
