from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BESession
from .tasks import run_bulk_extractor

@receiver(post_save, sender=BESession)
def be_session_post_save(sender, instance, **kwargs):
	# Run bulk_extractor after creation only, not after updates
	if kwargs['created']:
		run_bulk_extractor.delay(instance.pk)