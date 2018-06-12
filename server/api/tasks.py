from django.conf import settings
from celery import shared_task
from .models import BEConfig, BESession
import os
import subprocess


@shared_task
def run_bulk_extractor(transfer_uuid, transfer_source, disk_image):
    feature_file_dir = os.path.join(settings.MEDIA_ROOT, 'feature_files', transfer_uuid)
    if not os.path.exists(feature_file_dir):
        os.makedirs(feature_file_dir)
    cmd = ['bulk_extractor',
               '-o', 
               feature_file_dir,
               transfer_source]
    if not disk_image:
        cmd.insert(3, '-R')

    try:
        subprocess.check_output(cmd)
        return('Success!')
    except subprocess.CalledProcessError as e:
        return('Failure! Error output: {}'.format(e))
