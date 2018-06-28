from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BESession, RedactedSet
from .tasks import run_bulk_extractor, redact_remove_files


@receiver(post_save, sender=BESession)
def be_session_post_save(sender, instance, **kwargs):
    # Run bulk_extractor after creation only, not after updates
    if kwargs['created']:
        run_bulk_extractor.delay(instance.pk)


@receiver(post_save, sender=RedactedSet)
def redacted_session_post_save(sender, instance, **kwargs):
    # Run redaction after creation only, not after updates
    if kwargs['created']:
        if instance.redaction_type == 1:
            redact_remove_files.delay(instance.pk)
