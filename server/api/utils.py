from .models import BESession, File, Feature, RedactedSet
import datetime
import os
import subprocess
import sys
import time

# Import Objects.py
if "linux" in sys.platform:
    sys.path.append('/usr/share/bulk_extractor')
elif "darwin" in sys.platform:
    sys.path.append('/usr/local/share/bulk_extractor')
import Objects


def time_to_int(str_time):
    dt = time.mktime(datetime.datetime.strptime(
        str_time,
        "%Y-%m-%dT%H:%M:%S").timetuple())
    return dt


def user_friendly_feature_type(feature_file):
    """
    Return user-friendly feature type value for
    corresponding feature file. If no such label
    exists, return name of feature file.
    """
    if feature_file == 'pii.txt':
        return 'Social Security Number'
    elif feature_file == 'ccn.txt':
        return 'Credit card number'
    elif feature_file == 'telephone.txt':
        return 'Phone number'
    elif feature_file == 'email.txt':
        return 'Email address'
    elif feature_file == 'find.txt':
        return 'Regular expression'
    elif feature_file == 'url.txt':
        return 'URL'
    elif feature_file == 'domain.txt':
        return 'Domain'
    elif feature_file == 'rfc822.txt':
        return 'Email/HTTP header (RFC822)'
    elif feature_file == 'httplogs.txt':
        return 'HTTP log'
    elif feature_file == 'gps.txt':
        return 'GPS data'
    elif feature_file == 'exif.txt':
        return 'EXIF metadata'
    else:
        return feature_file


def carve_files(redacted_set_uuid, out_dir):
    """
    Carve allocated or all files from disk image
    to output directory using tsk_recover and return
    True if successful.
    """
    redacted_set = RedactedSet.objects.get(pk=redacted_set_uuid)
    be_session = redacted_set.be_session
    transfer_source = redacted_set.be_session.source_path
    unallocated = redacted_set.unallocated_files
    # Sanity check
    if not be_session.disk_image:
        print("Transfer source not a disk image. Shutting down.")
        return False
    # Create tsk_recover command
    if unallocated:
        cmd = ['tsk_recover', '-e', transfer_source, out_dir]
    else:
        cmd = ['tsk_recover', '-a', transfer_source, out_dir]
    # Run tsk_recover as subprocess
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print("tsk_recover error: {}".format(e))
        return False
    return True


def restore_dates_from_dfxml(file_dir, dfxml):
    """
    Rewrite last modified dates of files based
    on values recorded in a DFXML file.
    """
    for (event, obj) in Objects.iterparse(dfxml):

        # only work on FileObjects
        if not isinstance(obj, Objects.FileObject):
            continue

        # record filename
        dfxml_filename = obj.filename
        dfxml_filedate = int(time.time())  # default to current time

        # record last modified or last created date
        try:
            mtime = obj.mtime
            mtime = str(mtime)
        except Exception:
            pass

        try:
            crtime = obj.crtime
            crtime = str(crtime)
        except Exception:
            pass

        # fallback to created date if last modified doesn't exist
        if mtime and (mtime != 'None'):
            mtime = time_to_int(mtime[:19])
            dfxml_filedate = mtime
        elif crtime and (crtime != 'None'):
            crtime = time_to_int(crtime[:19])
            dfxml_filedate = crtime
        else:
            continue

        # rewrite last modified date of corresponding file in objects/files
        file_to_modify = os.path.join(file_dir, dfxml_filename)
        try:
            os.utime(file_to_modify, (dfxml_filedate, dfxml_filedate))
        except Exception as e:
            print("Error modifying modified date for {0}. Error: {1}".format(file_to_modify, e))


def parse_dfxml_to_db(be_session_uuid):
    be_session = BESession.objects.get(pk=be_session_uuid)
    dfxml_file = be_session.dfxml_path

    # Gather info for each FileObject and save to db
    for (event, obj) in Objects.iterparse(dfxml_file):

        # Only work on FileObjects
        if not isinstance(obj, Objects.FileObject):
            continue

        # Skip directories and links
        if obj.name_type:
            if obj.name_type != "r":
                continue

        # Create new File model instance
        filepath = obj.filename
        filename = os.path.basename(filepath)
        new_file = File.objects.create(
            filepath=filepath,
            filename=filename,
            be_session=be_session
        )

        # Gather file metadata
        file_info = dict()
        if obj.mtime:
            file_info['date_modified'] = obj.mtime
        if obj.crtime:
            file_info['date_created'] = obj.crtime
        if obj.ctime:
            file_info['date_created'] = obj.ctime
        if obj.unalloc:
            if obj.unalloc == 1:
                file_info['allocated'] = False

        # Save file metadata to model
        new_file.__dict__.update(file_info)
        new_file.save()


def parse_feature_file(feature_file, be_session_uuid):
    with open(feature_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Ignore commented lines
            if line.startswith(('#')):
                continue
            # Ignore blank lines
            if not line.strip():
                continue

            # Parse and clean up tab-separated lines
            DELIMITER = '\U0010001c'
            forensic_path = ''
            filepath = ''
            feature = ''
            context = ''
            try:
                (forensic_path, feature, context) = line.split('\t')
                if DELIMITER in forensic_path:
                    filepath = forensic_path.split(DELIMITER)[0]
                context = context.rstrip()  # strip trailing newline

                # Make filepath relative to match DFXML filename
                be_session = BESession.objects.get(pk=be_session_uuid)
                substr = be_session.source_path + '/'
                filepath = filepath.split(substr)[1]

                # Find matching file
                try:
                    matching_file = File.objects.get(
                        filepath=filepath,
                        be_session=be_session
                    )
                except File.DoesNotExist:
                    print("Matching file not found for", filepath)
                    continue

                # Update db
                Feature.objects.create(
                    feature_file=os.path.basename(feature_file),
                    forensic_path=forensic_path,
                    feature=feature,
                    context=context,
                    source_file=matching_file
                )
            except Exception:
                print("Error processing line in feature file", feature_file)


def parse_annotated_feature_file(feature_file, be_session_uuid):
    with open(feature_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Ignore commented lines
            if line.startswith(('#')):
                continue
            # Ignore blank lines
            if not line.strip():
                continue

            # Parse tab-separated lines
            try:
                (offset, feature, context, filepath, blockhash) = line.split('\t')

                # Find matching file
                be_session = BESession.objects.get(pk=be_session_uuid)
                try:
                    matching_file = File.objects.get(
                        filepath=filepath,
                        be_session=be_session
                    )

                # If matching file doesn't exist, match to placeholder
                # File instance for unallocated space instead
                except File.DoesNotExist:

                    # Check if placeholder already exists
                    try:
                        matching_file = File.objects.get(
                            filepath="<unallocated space>",
                            be_session=be_session
                        )
                        print("Matching unmatched feature to <unallocated space> placeholder")

                    # Create placeholder if doesn't exist
                    except File.DoesNotExist:
                        unallocated_placeholder = File.objects.create(
                            filepath="<unallocated space>",
                            filename="<unallocated space>",
                            allocated=False,
                            be_session=be_session
                        )
                        matching_file = unallocated_placeholder
                        print("Creating <unallocated space> placeholder for unmatched feature")

                # Update db
                Feature.objects.create(
                    feature_file=os.path.basename(feature_file).replace('annotated_', ''),
                    offset=offset,
                    feature=feature,
                    context=context,
                    source_file=matching_file
                )
            except Exception:
                print("Error reading line in feature file", feature_file)
