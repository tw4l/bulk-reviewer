from .models import BESession, File
from django.shortcuts import get_object_or_404
import os
import sys
import zipfile

# Import Objects.py
sys.path.append('/src/bulkext_scripts/')
import Objects


def unzip_transfer(zip_file, new_path):
    with open(zip_file, 'rb') as f:
        print("Unzipping file", zip_file)
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            print("    Extracting file", name)
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
        new_file = File.objects.create(filepath=filepath,
                                       filename=filename,
                                       be_session=be_session)

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
