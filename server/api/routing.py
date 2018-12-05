from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/sessions/$', consumers.SessionConsumer),
    url(r'^ws/features/$', consumers.FeatureConsumer),
    url(r'^ws/files/$', consumers.FileConsumer),
    url(r'^ws/redacted-sets/$', consumers.RedactedSetConsumer),
]
