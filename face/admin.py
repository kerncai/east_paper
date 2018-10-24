from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Face_images_upload)
admin.site.register(models.Face_check_results)
admin.site.register(models.Face_diff_results)
admin.site.register(models.Face_core_body_results)
