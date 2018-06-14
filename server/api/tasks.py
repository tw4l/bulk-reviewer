from django.conf import settings
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import BESession
from .utils import unzip_transfer, parse_dfxml_to_db

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
    if be_session.in_process:
        return('Bulk Extractor already in process for this session.')
    if be_session.processing_complete:
        return('Bulk Extractor has already completed for this session.')

    # Mark session as in process
    be_session.in_process = True
    be_session.save()

    # Uncompress uploaded zip file
    if not disk_image:
        extracted_files_path = os.path.join(settings.MEDIA_ROOT,
                                            'extracted_transfers',
                                            be_session_uuid)
        if not os.path.exists(extracted_files_path):
            os.makedirs(extracted_files_path)
        try:
            unzip_transfer(transfer_source, extracted_files_path)
            be_session.extracted_transfer = extracted_files_path
            be_session.save()
        except:
            return('Error extracting transfer zip file')

    # Create feature file output directory
    feature_file_dir = os.path.join(settings.MEDIA_ROOT,
                                    'feature_files',
                                    be_session_uuid)
    if not os.path.exists(feature_file_dir):
        os.makedirs(feature_file_dir)

    # Create bulk_extractor command
    if not disk_image:
        transfer_source = be_session.extracted_transfer
    cmd = ['bulk_extractor',
           '-o',
           feature_file_dir,
           '-E',
           'accts',
           '-e',
           'email',
           '-e',
           'pdf'
           '-S',
           'jpeg_carve_mode=0',
           '-S',
           'unzip_carve_mode=0',
           '-S',
           'unrar_carve_mode=0',
           transfer_source]
    if not disk_image:
        cmd.insert(3, '-R')

    # Run bulk_extractor via subprocess and update model if successful
    try:
        subprocess.check_output(cmd)
        be_session.be_complete = True
        be_session.feature_files_path = feature_file_dir
        be_session.save()

        # Create dfxml
        dfxml_dir = os.path.join(settings.MEDIA_ROOT,
                                 'dfxml')
        dfxml_path = os.path.join(dfxml_dir,
                                  be_session_uuid + '_dfxml.xml')
        if not os.path.exists(dfxml_dir):
            os.makedirs(dfxml_dir)

        if disk_image:
            cmd = ['fiwalk',
                   '-X',
                   dfxml_path,
                   transfer_source]

            try:
                subprocess.check_output(cmd)
                be_session.dfxml_path = dfxml_path
                be_session.dfxml = True
                be_session.save()
            except subprocess.CalledProcessError as e:
                print('fiwalk failure', e)

        else:
            cmd = 'cd "{0}" && python3 /src/bulkext_scripts/walk_to_dfxml.py > {1}'.format(transfer_source, dfxml_path)
            try:
                subprocess.call(cmd, shell=True)
                be_session.dfxml_path = dfxml_path
                be_session.dfxml = True
                be_session.save()
            except subprocess.CalledProcessError as e:
                print('walk_to_dfxml.py failure!', e)

        # Annotate feature files
        if disk_image:
            annotated_feature_file_dir = os.path.join(settings.MEDIA_ROOT,
                                                      'annotated_feature_files',
                                                      be_session_uuid)
            if not os.path.exists(annotated_feature_file_dir):
                os.makedirs(annotated_feature_file_dir)
            cmd = ['python3',
                   '/src/bulkext_scripts/identify_filenames.py',
                   '--all',
                   '--xmlfile',
                   be_session.dfxml_path,
                   feature_file_dir,
                   annotated_feature_file_dir]
            try:
                subprocess.check_output(cmd)
                be_session.features_annotated = True
                be_session.annotated_feature_files_path = annotated_feature_file_dir
                be_session.save()
            except subprocess.CalledProcessError as e:
                print('identify_filenames failure!', e)

        # Read files into db from dfxml
        parse_dfxml_to_db(be_session_uuid)

        # Mark processing as complete in db
        be_session.processing_complete = True
        be_session.save()
        return('Success!')
    except subprocess.CalledProcessError as e:
        return('Failure! Error output: {}'.format(e))
