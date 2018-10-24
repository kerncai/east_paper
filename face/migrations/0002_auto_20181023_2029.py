# Generated by Django 2.0.6 on 2018-10-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='face_images_upload',
            name='face_image_path1',
            field=models.ImageField(blank=True, null=True, upload_to='upload/%Y%m%d43470', verbose_name='上传照片'),
        ),
        migrations.AlterField(
            model_name='face_images_upload',
            name='face_image_path2',
            field=models.ImageField(blank=True, null=True, upload_to='upload/%Y%m%d83874', verbose_name='对比照片'),
        ),
    ]
