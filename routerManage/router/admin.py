from django.contrib import admin

# Register your models here.

from router import models
admin.site.register(models.IP)
admin.site.register(models.User)
admin.site.register(models.Time)
admin.site.register(models.Error)