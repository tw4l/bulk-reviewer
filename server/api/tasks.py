from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import BESession, File, Feature, RedactedSet
from . import utils

import csv
import datetime
import magic
import os
import shutil
import subprocess
import zipfile

logger = get_task_logger(__name__)


@shared_task
def run_bulk_extractor(be_session_uuid):
    """
    Process source directory or disk image:
    1. Run bulk_extractor
    2. Create DFXML of source and read into db
    3. Annotate feature files (disk images only)
    4. Read feature files into db
    5. Identify MIME types (directories only)
    6. Extract named entities (optional, directories only)
    7. Mark processing as complete in db
    """

    # Make sure stoplists are extracted
    stoplist_zip = '/usr/share/bulk_extractor/stoplists.zip'
    stoplist_dir = '/usr/share/bulk_extractor/stoplists'
    if not os.path.isdir(stoplist_dir):
        with zipfile.ZipFile(stoplist_zip, 'r') as zip_ref:
            zip_ref.extractall('/usr/share/bulk_extractor/')

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
           '-w',
           '/usr/share/bulk_extractor/stoplists/combined-url.txt',
           '-w',
           '/usr/share/bulk_extractor/stoplists/combined-email.txt',
           '-w',
           '/usr/share/bulk_extractor/stoplists/combined-telephone.txt',
           '-w',
           '/usr/share/bulk_extractor/stoplists/combined-ccn.txt',
           '-w',
           '/usr/share/bulk_extractor/stoplists/domain.txt',
           '-x',
           'accts_lg',
           '-x',
           'email_lg',
           '-x',
           'gps_lg',
           '-x',
           'lightgrep',
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
           'ssn_mode={}'.format(str(be_config.ssn_mode)),
           '-S',
           'jpeg_carve_mode=0',
           transfer_source]
    if not disk_image:
        cmd.insert(35, '-R')
    if be_config.regex_file:
        cmd.insert(1, '-F')
        cmd.insert(2, be_config.regex_file.path)
    if be_config.pii_scanners is False:
        cmd.insert(17, '-x')
        cmd.insert(18, 'accts')
    if be_config.web_scanners is False:
        cmd.insert(17, '-x')
        cmd.insert(18, 'net')
        cmd.insert(17, '-x')
        cmd.insert(18, 'httplogs')
    if be_config.exif_gps_scanners is False:
        cmd.insert(17, '-x')
        cmd.insert(18, 'exif')
        cmd.insert(17, '-x')
        cmd.insert(18, 'gps')

    # Run bulk_extractor via subprocess and update model if successful
    try:
        logger.info('Bulk Extractor command: {}'.format(cmd))  # FOR DEBUGGING
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
            # Skip stoplist results
            if "_stopped" in feature_file:
                continue
            # Skip web-related feature files if web scanners disabled
            if be_config.web_scanners is False:
                if "url" in feature_file:
                    continue
                if "domain" in feature_file:
                    continue
                if "rfc822" in feature_file:
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
            # Skip stoplist results
            if "_stopped" in feature_file:
                continue
            # Skip web-related feature files if web scanners disabled
            if be_config.web_scanners is False:
                if "url" in feature_file:
                    continue
                if "domain" in feature_file:
                    continue
                if "rfc822" in feature_file:
                    continue
            # Parse file and write features into db
            utils.parse_feature_file(ff_abspath, be_session_uuid)

    # Get named entities (directories only)
    if not disk_image:
        if be_session.named_entity_extraction is True:
            utils.get_named_entities(be_session_uuid)

    # Mark processing as complete in db
    be_session.processing_complete = True
    be_session.save()


@shared_task
def update_features(features, cleared):
    """
    Update cleared status in db for each feature in list
    """
    for f in Feature.objects.filter(pk__in=features):
        f.cleared = cleared
        f.save()  # call save to trigger post_save signal


@shared_task
def create_csv_reports(be_session_uuid):
    """
    Create two CSV reports, sorted by file then feature type:
    1. Features confirmed as sensitive
    2. Dismissed/unconfirmed features
    """

    # Set variables
    be_session = BESession.objects.get(pk=be_session_uuid)

    # Create output directory
    log_dir = os.path.join(settings.MEDIA_ROOT,
                           'csv_reports',
                           be_session_uuid)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Write log file of redacted features
    log_name = be_session.name + '_to_redact.csv'
    log_file = os.path.join(log_dir, log_name)
    with open(log_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        # Write header
        writer.writerow(['Source file', 'mimetype', 'Match type', 'Match text', 'Context', 'Note'])
        # Write lines for Features marked as redacted
        redacted_features = Feature.objects.filter(source_file__be_session=be_session_uuid).filter(cleared=False)
        for f in redacted_features:
            # Human-friendly feature type
            feature_type = utils.user_friendly_feature_type(f.feature_file)
            # Write row
            writer.writerow([f.source_file.filepath, f.source_file.mime_type, feature_type, f.feature, f.context, f.note])

    # Write log file of dismissed features
    log_name = be_session.name + '_dismissed.csv'
    log_file = os.path.join(log_dir, log_name)
    with open(log_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        # Write header
        writer.writerow(['Source file', 'Match type', 'Match text', 'Context', 'Note'])
        # Write lines for Features marked as cleared
        dismissed_features = Feature.objects.filter(source_file__be_session=be_session_uuid).filter(cleared=True)
        for f in dismissed_features:
            # Human-friendly feature type
            feature_type = utils.user_friendly_feature_type(f.feature_file)
            # Write row
            writer.writerow([f.source_file.filepath, feature_type, f.feature, f.context, f.note])


@shared_task
def export_files(redacted_set_uuid):
    """
    Create export containing:
    1. 'clean' directory: files with no sensitive features
    2. 'to_redact' directory: files with sensitive features
    3. CSV exports
    """

    # Set variables
    redacted_set = RedactedSet.objects.get(pk=redacted_set_uuid)
    transfer_source = redacted_set.be_session.source_path
    disk_image = redacted_set.be_session.disk_image
    dfxml = redacted_set.be_session.dfxml_path
    be_session_uuid = str(redacted_set.be_session.uuid)
    be_session = BESession.objects.get(pk=be_session_uuid)

    # Create temp working space
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    working_dir = os.path.join(temp_dir, 'clean')
    # Only create output dir for disk images
    if disk_image:
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

    # Create export directory and save as RedactedSet name
    export_name = be_session.name + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
    redacted_set.name = export_name
    redacted_set.save()
    session_output = '/data/exports/' + export_name
    # Overwrite path if exists
    if os.path.exists(session_output):
        shutil.rmtree(session_output)
    os.makedirs(session_output)
    to_redact_dir = os.path.join(session_output, 'to_redact')
    os.makedirs(to_redact_dir)

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
    files_with_redacted_features = File.objects.distinct().filter(be_session=redacted_set.be_session).filter(features__cleared=False)
    for f in files_with_redacted_features:
        if f.filepath not in redacted_list:
            redacted_list.append(f.filepath)

    # Move files in redacted_list to to_redact_dir
    for f in redacted_list:
        filepath = os.path.join(working_dir, f)
        try:
            shutil.move(filepath, to_redact_dir)
        except Exception as e:
            logger.error("Error moving file {0} from working directory for redacted set {1}. Error: {2}".format(filepath, redacted_set_uuid, e))
            redacted_set.processing_failure = True
            redacted_set.save()
            return

    # Move clean files to clean_dir
    try:
        shutil.move(working_dir, session_output)
    except Exception:
        logger.error("Error moving redacted set to {}".format(session_output))
        redacted_set.processing_failure = True
        redacted_set.save()
        return

    # Copy CSV reports to output dir
    csv_reports_dir = os.path.join(settings.MEDIA_ROOT,
                                   'csv_reports',
                                   be_session_uuid)
    target_dir = os.path.join(session_output, 'reports')
    shutil.copytree(csv_reports_dir, target_dir)

    # Mark as completed in database
    redacted_set.processing_complete = True
    redacted_set.save()
    return
