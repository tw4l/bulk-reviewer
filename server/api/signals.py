import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BESession, RedactedSet, Feature
from . import tasks


@receiver(post_save, sender=Feature, dispatch_uid='update_feature_status_listeners')
def update_feature_status_listeners(sender, instance, **kwargs):
    # Send message only on update, not on create
    if not kwargs['created']:
        # Send update to client when Feature is modified in a given Session
        group_name = 'features'

        message = {
            'uuid': str(instance.uuid),
            'cleared': instance.cleared,
            'note': instance.note,
        }

        channel_layer = channels.layers.get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )


@receiver(post_save, sender=BESession)
def be_session_post_save(sender, instance, **kwargs):
    # Run bulk_extractor after creation only, not after updates
    if kwargs['created']:
        tasks.run_bulk_extractor.delay(instance.pk)

    # Send message to sessions group after every save
    group_name = 'sessions'

    message = {
        'uuid': str(instance.uuid),
        'name': instance.name,
        'complete': instance.processing_complete,
        'failure': instance.processing_failure,
    }

    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_message',
            'message': message
        }
    )


@receiver(post_save, sender=RedactedSet)
def redacted_session_post_save(sender, instance, **kwargs):
    # Run redaction after creation only, not after updates
    if kwargs['created']:
        # Create csv reports
        be_session_uuid = str(instance.be_session.uuid)
        output = tasks.create_csv_reports.delay(be_session_uuid)
        output.get()

        # Create file/report export
        if instance.redaction_type == 1:
            tasks.export_files.delay(instance.pk)

    # Send update to client when Redacted Set is saved/updated
    else:
        group_name = 'redacted-sets'

        message = {
            'uuid': str(instance.uuid),
            'name': instance.name,
            'complete': instance.processing_complete,
            'failure': instance.processing_failure,
        }

        channel_layer = channels.layers.get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )
