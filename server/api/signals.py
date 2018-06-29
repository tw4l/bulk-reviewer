from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BESession, RedactedSet
from . import tasks


@receiver(post_save, sender=BESession)
def be_session_post_save(sender, instance, **kwargs):
    # Run bulk_extractor after creation only, not after updates
    if kwargs['created']:
        tasks.run_bulk_extractor.delay(instance.pk)


@receiver(post_save, sender=RedactedSet)
def redacted_session_post_save(sender, instance, **kwargs):
    # Run redaction after creation only, not after updates
    if kwargs['created']:
        # Create log
        tasks.create_redaction_log.delay(instance.pk)
        # Create redacted set
        if instance.redaction_type == 1:
            tasks.redact_remove_files.delay(instance.pk)
