import uuid
from django.db import models


class Transfer(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    description = models.CharField(
        max_length=200,
        blank=True
    )
    source_path = models.FileField(upload_to='transfers/')
    disk_image = models.BooleanField(default=False)
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.source_path))


class BEConfig(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    # TODO: scanners, alert list, stop list, ssn_mode, regex

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.name))


class BESession(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    transfer = models.ForeignKey(
        Transfer,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    be_config = models.ForeignKey(
        BEConfig,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    extracted_transfer = models.TextField(
        null=True,
        blank=True
    )
    feature_files_path = models.TextField(
        null=True,
        blank=True
    )
    annotated_feature_files_path = models.TextField(
        null=True,
        blank=True
    )
    dfxml_path = models.TextField(
        null=True,
        blank=True
    )
    in_process = models.BooleanField(default=False)
    be_complete = models.BooleanField(default=False)
    features_annotated = models.BooleanField(default=False)
    dfxml = models.BooleanField(default=False)
    processing_complete = models.BooleanField(default=False)

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.name))


class File(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    filename = models.TextField(blank=True)
    filepath = models.TextField(blank=True)
    date_modified = models.CharField(
        max_length=50,
        blank=True
    )
    date_created = models.CharField(
        max_length=50,
        blank=True
    )
    redacted = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    file_type = models.CharField(
        max_length=200,
        blank=True
    )
    allocated = models.BooleanField(default=True)
    be_session = models.ForeignKey(
        BESession,
        related_name="files",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.filename))


class Feature(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    feature_file = models.CharField(max_length=50)
    forensic_path = models.CharField(max_length=100, null=True)
    offset = models.IntegerField(null=True)
    feature = models.TextField(null=True)
    context = models.TextField(null=True)
    source_file = models.ForeignKey(
        File,
        related_name="features",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.feature))
