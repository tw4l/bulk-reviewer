from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import BESession, File, Feature, RedactedSet
from . import utils

import magic
import os
import shutil
import subprocess

logger = get_task_logger(__name__)


@shared_task
def run_bulk_extractor(be_session_uuid):

    # Set variables
    be_session = BESession.objects.get(pk=be_session_uuid)
    transfer_source = be_session.source_path
    disk_image = be_session.disk_image
    be_config = be_session.be_config

    # Create feature file output directory
    feature_files_path = os.path.join(settings.MEDIA_ROOT,
                                      'feature_files',
                                      be_session_uuid)
    if not os.path.exists(feature_files_path):
        os.makedirs(feature_files_path)

    # Create bulk_extractor command
    cmd = ['bulk_extractor',
           '-o',
           feature_files_path,
           '-x',
           'accts',
           '-x',
           'email',
           '-x',
           'gps',
           '-x',
           'find',
           '-x',
           'windirs',
           '-x',
           'winpe',
           '-x',
           'winlnk',
           '-x',
           'winprefetch',
           '-x',
           'base16_lg',
           '-S',
           'ssn_mode={}'.format(be_config.ssn_mode),
           '-S',
           'jpeg_carve_mode=0',
           transfer_source]
    if not disk_image:
        cmd.insert(25, '-R')
    if be_config.regex_file:
        cmd.insert(1, '-F')
        cmd.insert(2, be_config.regex_file.path)

    # Run bulk_extractor via subprocess and update model if successful
    try:
        subprocess.check_output(cmd)
        be_session.feature_files_path = feature_files_path
        be_session.save()
    except subprocess.CalledProcessError as e:
        be_session.processing_failure = True
        be_session.save()
        logger.error('bulk_extractor unsuccessful for session {0}. Error output: {1}'.format(be_session_uuid, e))
        return

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
            be_session.save()
        except subprocess.CalledProcessError as e:
            be_session.processing_failure = True
            be_session.save()
            logger.error('fiwalk unable to create DFXML for session {0}. Error output: {1}'.format(be_session_uuid, e))
            return

    else:
        cmd = 'cd "{0}" && python3 /usr/share/bulk_extractor/walk_to_dfxml.py > "{1}"'.format(transfer_source, dfxml_path)
        try:
            subprocess.call(cmd, shell=True)
            be_session.dfxml_path = dfxml_path
            be_session.save()
        except subprocess.CalledProcessError as e:
            be_session.processing_failure = True
            be_session.save()
            logger.error('walk_to_dfxml unable to create DFXML for session {0}. Error output: {1}'.format(be_session_uuid, e))
            return

    # Annotate feature files
    if disk_image:
        annotated_feature_files_path = os.path.join(settings.MEDIA_ROOT,
                                                    'annotated_feature_files',
                                                    be_session_uuid)
        if not os.path.exists(annotated_feature_files_path):
            os.makedirs(annotated_feature_files_path)
        cmd = ['python3',
               '/usr/share/bulk_extractor/identify_filenames.py',
               '--all',
               '--xmlfile',
               be_session.dfxml_path,
               feature_files_path,
               annotated_feature_files_path]
        try:
            subprocess.check_output(cmd)
            be_session.annotated_feature_files_path = annotated_feature_files_path
            be_session.save()
        except subprocess.CalledProcessError as e:
            be_session.processing_failure = True
            be_session.save()
            logger.error('identify_filenames.py unable to annotated feature files for session {0}. Error output: {1}'.format(be_session_uuid, e))
            return

    # Read files into db from dfxml
    utils.parse_dfxml_to_db(be_session_uuid)

    # Identify mime types for uploaded files
    if not disk_image:
        files_to_identify = File.objects.filter(be_session=be_session_uuid)
        for f in files_to_identify:
            fpath = os.path.join(transfer_source, f.filepath)
            try:
                mime_type = magic.from_file(fpath, mime=True)
                f.mime_type = mime_type
                f.save()
            except Exception:
                logger.warning('Error determining mime type for {0}'.format(fpath))

    # Read feature files into db
    if disk_image:
        for feature_file in os.listdir(annotated_feature_files_path):
            # Absolute path for file
            ff_abspath = os.path.join(annotated_feature_files_path, feature_file)
            # Skip empty files
            if not os.path.getsize(ff_abspath) > 0:
                continue
            # Parse file and write features into db
            utils.parse_annotated_feature_file(ff_abspath, be_session_uuid)
    else:
        for feature_file in os.listdir(feature_files_path):
            # Absolute path for file
            ff_abspath = os.path.join(feature_files_path, feature_file)
            # Skip empty files
            if not os.path.getsize(ff_abspath) > 0:
                continue
            # Skip non-txt files
            if not feature_file.endswith(".txt"):
                continue
            # Skip histograms
            if "histogram" in feature_file:
                continue
            if "url_" in feature_file:
                continue
            # Skip zip-related files
            if "zip" in feature_file:
                continue
            # Skip json
            if "json" in feature_file:
                continue
            # Parse file and write features into db
            utils.parse_feature_file(ff_abspath, be_session_uuid)

    # Mark processing as complete in db
    be_session.processing_complete = True
    be_session.save()


@shared_task
def create_redaction_log(redacted_set_uuid):

    # Set variables
    redacted_set = RedactedSet.objects.get(pk=redacted_set_uuid)

    # Create output directory
    log_dir = '/data/logs/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Write log file
    log_name = redacted_set.name + '_redaction_log.txt'
    log_file = os.path.join(log_dir, log_name)
    with open(log_file, 'w') as log:
        # Write header
        log.write('Bulk Redactor Redaction Log\n\n')
        log.write('Session Information:\n')
        log.write('-------------------\n')
        log.write('Session name: {}\n'.format(redacted_set.be_session.name))
        log.write('Session UUID: {}\n'.format(str(redacted_set.be_session.uuid)))
        log.write('Redacted set name: {}\n'.format(redacted_set.name))
        log.write('Redacted Set UUID: {}\n'.format(str(redacted_set.uuid)))
        log.write('Source files: {}\n'.format(redacted_set.be_session.source_path))
        log.write('Disk image?: {}\n'.format(str(redacted_set.be_session.disk_image)))
        log.write('Bulk Extractor configuration: {}\n'.format(redacted_set.be_session.be_config.name))
        log.write('Bulk Extractor configuration UUID: {}\n'.format(str(redacted_set.be_session.be_config.uuid)))
        log.write('\n\n')
        # Write lines for Features marked as redacted
        log.write('Features marked for redaction:\n')
        log.write('--------------------------\n')
        redacted_features = Feature.objects.filter(source_file__be_session=redacted_set.be_session).filter(cleared=False)
        if not redacted_features:
            log.write('No features marked for redaction.')
        log.write('Feature file\tFeature\tContext\tSource file\tNote\n')
        for f in redacted_features:
            log.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(f.feature_file, f.feature, f.context, f.source_file.filepath, f.redaction_note))
    # Update db
    redacted_set.redaction_log = log_file
    redacted_set.save()


@shared_task
def redact_remove_files(redacted_set_uuid):

    # Set variables
    redacted_set = RedactedSet.objects.get(pk=redacted_set_uuid)
    transfer_source = redacted_set.be_session.source_path
    disk_image = redacted_set.be_session.disk_image
    dfxml = redacted_set.be_session.dfxml_path

    # Create temp working space
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    working_dir = os.path.join(temp_dir, redacted_set.name)
    # Only create output dir for disk images
    if disk_image:
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

    # Carve and/or copy set of files to temporary working directory
    if disk_image:
        # Carve files
        carve_files = utils.carve_files(redacted_set_uuid, working_dir)
        if not carve_files:
            logger.error('Unable to carve files from disk image for redacted set {0}.'.format(redacted_set_uuid))
            redacted_set.processing_failure = True
            redacted_set.save()
            return
        # Restore modified dates to values on disk
        utils.restore_dates_from_dfxml(working_dir, dfxml)
    else:
        try:
            shutil.copytree(transfer_source, working_dir)
        except Exception as e:
            logger.error("Unable to copy source files to working dir for redacted set {0}. Error: {1}".format(redacted_set_uuid, e))
            redacted_set.processing_failure = True
            redacted_set.save()
            return

    # Build list of files to remove from working dir, including
    # all files with at least one feature not marked cleared
    redacted_list = list()
    # Include files where any features have been marked for redaction
    files_with_redacted_features = File.objects.distinct().filter(be_session=redacted_set.be_session).filter(features__cleared=False)
    for f in files_with_redacted_features:
        if f.filepath not in redacted_list:
            redacted_list.append(f.filepath)

    # Remove files in redacted_list from working dir
    for f in redacted_list:
        filepath = os.path.join(working_dir, f)
        try:
            os.remove(filepath)
        except Exception as e:
            logger.error("Error deleting file {0} from working directory for redacted set {1}. Error: {2}".format(filepath, redacted_set_uuid, e))
            redacted_set.processing_failure = True
            redacted_set.save()
            return

    # Move redacted set to data/redacted
    if not os.path.exists('/data/redacted/'):
        os.makedirs('/data/redacted/')
    try:
        redacted_dir = '/data/redacted/' + redacted_set.name
        shutil.move(working_dir, redacted_dir)
    except Exception:
        logger.error("Error moving redacted set to {}".format(redacted_dir))
        redacted_set.processing_failure = True
        redacted_set.save()
        return

    # Mark as completed in database
    redacted_set.processing_complete = True
    redacted_set.save()
    return
