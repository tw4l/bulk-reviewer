from .models import BESession, File, Feature
from django.shortcuts import get_object_or_404
import os
import sys
import zipfile

# Import Objects.py
sys.path.append('/src/bulkext_scripts/')
import Objects


def unzip_transfer(zip_file, new_path):
    with open(zip_file, 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, new_path)


def parse_dfxml_to_db(be_session_uuid):
    be_session = get_object_or_404(BESession, pk=be_session_uuid)
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
            DELIM = '\U0010001c'
            forensic_path = ''
            filepath = ''
            feature = ''
            context = ''
            try:
                (forensic_path, feature, context) = line.split('\t')
                if DELIM in forensic_path:
                    filepath = forensic_path.split(DELIM)[0]
                context = context.rstrip()  # strip trailing newline

                # Make filepath relative to match DFXML filename
                be_session = get_object_or_404(BESession, pk=be_session_uuid)
                substr = str(be_session.uuid) + '/'
                filepath = filepath.split(substr)[1]

                # Find matching file
                try:
                    matching_file = get_object_or_404(
                        File,
                        filepath=filepath,
                        be_session=be_session)
                    print("Matching file:", str(matching_file.filename))
                except:
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
            except:
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
                be_session = get_object_or_404(BESession, pk=be_session_uuid)
                try:
                    matching_file = get_object_or_404(
                        File,
                        filepath=filepath,
                        be_session=be_session)
                    print("Matching file:", str(matching_file.filename))
                except:
                    print("Matching file not found for", filepath)
                    continue

                # Update db
                Feature.objects.create(
                    feature_file=os.path.basename(feature_file),
                    offset=int(offset),
                    feature=feature,
                    context=context,
                    source_file=matching_file
                )
            except:
                print("Error reading line in feature file", feature_file)
