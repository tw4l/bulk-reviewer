from .models import BESession, File, Feature
import os
import sys

# Import Objects.py
if "linux" in sys.platform:
    sys.path.append('/usr/share/bulk_extractor')
elif "darwin" in sys.platform:
    sys.path.append('/usr/local/share/bulk_extractor')
import Objects


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
                    feature_file=os.path.basename(feature_file),
                    offset=int(offset),
                    feature=feature,
                    context=context,
                    source_file=matching_file
                )
            except Exception:
                print("Error reading line in feature file", feature_file)
