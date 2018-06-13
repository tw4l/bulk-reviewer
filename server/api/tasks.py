from django.conf import settings
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import BESession

import datetime
import os
import subprocess


@shared_task
def run_bulk_extractor(be_session_uuid):

    # Get necessary information
    be_session = get_object_or_404(BESession, pk=be_session_uuid)
    transfer_source = be_session.transfer.source_path.path
    disk_image = be_session.transfer.disk_image
    # be_config = str(be_session.be_config.uuid)

    # Sanity check
    if be_session.processing_complete:
        return('Bulk Extractor has already completed for this session.')

    # Create feature file output directory
    feature_file_dir = os.path.join(settings.MEDIA_ROOT,
                                    'feature_files',
                                    be_session_uuid)
    if not os.path.exists(feature_file_dir):
        os.makedirs(feature_file_dir)

    # Create bulk_extractor command
    cmd = ['bulk_extractor',
           '-o',
           feature_file_dir,
           transfer_source]
    if not disk_image:
        cmd.insert(3, '-R')

    # Run bulk_extractor via subprocess and update model if successful
    try:
        subprocess.check_output(cmd)
        be_session.be_finished = datetime.datetime.now()
        be_session.be_feature_files = feature_file_dir
        be_session.processing_complete = True
        be_session.save()

        # Run identify_filenames to annotate feature files for disk images
        annotated_feature_file_dir = os.path.join(settings.MEDIA_ROOT,
                                    'annotated_feature_files',
                                    be_session_uuid)
        if not os.path.exists(annotated_feature_file_dir):
            os.makedirs(annotated_feature_file_dir)
        if disk_image:
            cmd = ['python3',
                   '/src/bulkext_scripts/identify_filenames.py',
                   '--all',
                   feature_file_dir,
                   annotated_feature_file_dir]
            try:
                subprocess.check_output(cmd)
                be_session.annotated_be_feature_files = annotated_feature_file_dir
                be_session.save()
            except subprocess.CalledProcessError as e:
                print('identify_filenames failure!')

        return('Success!')
    except subprocess.CalledProcessError as e:
        return('Failure! Error output: {}'.format(e))
