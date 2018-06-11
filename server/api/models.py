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
        return str(self.uuid)


class BEConfig(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    # TODO: scanners, alert list, stop list, ssn_mode, regex

    def __str__(self):
        return str(self.name)


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
    be_feature_files = models.TextField(
        null=True,
        blank=True
    )
    annotated_be_feature_files = models.TextField(
        null=True,
        blank=True
    )
    be_started = models.DateTimeField(
        null=True,
        blank=True
    )
    be_finished = models.DateTimeField(
        null=True,
        blank=True
    )
    processing_complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)


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
        return str(self.uuid)


class Feature(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    feature_file = models.CharField(max_length=50)
    forensic_path = models.CharField(max_length=100)
    offset = models.IntegerField()
    feature = models.TextField()
    context = models.TextField()
    source_file = models.ForeignKey(
        File,
        related_name="features",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.uuid)
