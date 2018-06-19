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
    SSN_CHOICES = (
        (0, 'Labeled "SSN:" (strictest)'),
        (1, 'No SSN, dashes required (default)'),
        (2, 'No dashes required (least strict)'),
    )
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    regex_file = models.FileField(
        upload_to='regex_files/',
        null=True,
        blank=True
    )
    ssn_mode = models.IntegerField(
        choices=SSN_CHOICES,
        default=1
    )
    # TODO: SIN, scanners, alert list, stop list

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
    extracted_transfer = models.TextField(blank=True)
    feature_files_path = models.TextField(blank=True)
    annotated_feature_files_path = models.TextField(blank=True)
    dfxml_path = models.TextField(blank=True)
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
    redact_file = models.BooleanField(default=False)
    redaction_note = models.TextField(blank=True)
    mime_type = models.CharField(
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
    forensic_path = models.CharField(
        max_length=100,
        blank=True
    )
    offset = models.IntegerField(
        null=True,
        blank=True
    )
    feature = models.TextField(blank=True)
    context = models.TextField(blank=True)
    redact_feature = models.BooleanField(default=False)
    redaction_note = models.TextField(blank=True)
    source_file = models.ForeignKey(
        File,
        related_name="features",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.feature))


class RedactedSet(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    log_only = models.BooleanField(default=False)
    redacted_set_path = models.TextField(blank=True)
    be_session = models.ForeignKey(
        BESession,
        related_name="redacted_sets",
        on_delete=models.CASCADE
    )
