# Generated by Django 2.0.6 on 2018-09-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_image_path',
            field=models.FileField(blank=True, null=True, upload_to='upload/%Y%m%d51994', verbose_name='图像路径'),
        ),
    ]
