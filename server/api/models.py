import uuid
from django.db import models


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
    source_path = models.FilePathField(
        path='/data/transfers/',
        allow_folders=True
    )
    disk_image = models.BooleanField(default=False)
    be_config = models.ForeignKey(
        BEConfig,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    feature_files_path = models.TextField(blank=True)
    annotated_feature_files_path = models.TextField(blank=True)
    dfxml_path = models.TextField(blank=True)
    started = models.DateTimeField(auto_now_add=True)
    processing_failure = models.BooleanField(default=False)
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
    cleared = models.BooleanField(default=False)
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
    forensic_path = models.TextField(blank=True)
    offset = models.IntegerField(
        null=True,
        blank=True
    )
    feature = models.TextField(blank=True)
    context = models.TextField(blank=True)
    redact_feature = models.BooleanField(default=False)
    redaction_note = models.TextField(blank=True)
    cleared = models.BooleanField(default=False)
    source_file = models.ForeignKey(
        File,
        related_name="features",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.feature))


class RedactedSet(models.Model):
    REDACTION_CHOICES = (
        (0, 'Log only'),
        (1, 'Remove files'),
        (2, 'Redact features (scrub)'),
        (3, 'Redact features (replace)'),
        (4, 'Redact features within disk image'),
    )
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        unique=True
    )
    redaction_type = models.IntegerField(
        choices=REDACTION_CHOICES,
        default=1
    )
    unallocated_files = models.BooleanField(default=False)
    redacted_set_path = models.TextField(blank=True)
    processing_failure = models.BooleanField(default=False)
    processing_complete = models.BooleanField(default=False)
    redaction_log = models.TextField(blank=True)
    be_session = models.ForeignKey(
        BESession,
        related_name="redacted_sets",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return('{0}: {1}'.format(str(self.uuid), self.name))
