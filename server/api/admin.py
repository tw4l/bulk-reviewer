from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.BEConfig)
admin.site.register(models.BESession)
admin.site.register(models.File)
admin.site.register(models.Feature)
admin.site.register(models.RedactedSet)
admin.site.register(models.User, UserAdmin)
