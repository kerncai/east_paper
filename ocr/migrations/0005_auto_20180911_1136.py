# Generated by Django 2.0.6 on 2018-09-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0004_auto_20180911_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_action_type',
            field=models.IntegerField(choices=[(0, '身份证'), (1, '名片')], verbose_name='识别动作'),
        ),
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_image_path',
            field=models.FileField(blank=True, null=True, upload_to='upload/%Y%m%d71388', verbose_name='身份证正面(国徽)/名片'),
        ),
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_image_path1',
            field=models.FileField(blank=True, null=True, upload_to='upload/%Y%m%d84828', verbose_name='身份证反面'),
        ),
    ]
