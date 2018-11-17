from django.contrib import admin

from . import models

admin.site.register(models.BEConfig)
admin.site.register(models.BESession)
admin.site.register(models.File)
admin.site.register(models.Feature)
admin.site.register(models.RedactedSet)
