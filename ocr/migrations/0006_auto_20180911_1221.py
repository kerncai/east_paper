# Generated by Django 2.0.6 on 2018-09-11 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0005_auto_20180911_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='IDcard_check_results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcard_action_user', models.CharField(max_length=255, null=True, verbose_name='执行者')),
                ('authority', models.CharField(max_length=255, null=True, verbose_name='签发机关')),
                ('valid_date', models.CharField(max_length=255, null=True, verbose_name='有效期限')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='姓名')),
                ('sex', models.CharField(max_length=255, null=True, verbose_name='性别')),
                ('birth', models.CharField(max_length=255, null=True, verbose_name='出生年月')),
                ('nation', models.CharField(max_length=255, null=True, verbose_name='民族')),
                ('num', models.CharField(max_length=255, null=True, verbose_name='公民身份号码')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='住址')),
                ('idcard_check_results_status', models.IntegerField(default=0, verbose_name='检测结果')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
            ],
            options={
                'verbose_name_plural': '身份证识别',
                'verbose_name': '身份证识别',
                'db_table': 'IDcard_check_results',
            },
        ),
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_image_path',
            field=models.FileField(blank=True, null=True, upload_to='upload/%Y%m%d34761', verbose_name='身份证正面(国徽)/名片'),
        ),
        migrations.AlterField(
            model_name='ocr_images_upload',
            name='ocr_image_path1',
            field=models.FileField(blank=True, null=True, upload_to='upload/%Y%m%d33888', verbose_name='身份证反面'),
        ),
        migrations.AddField(
            model_name='idcard_check_results',
            name='idcard_image_upload_relation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OCR', to='ocr.Ocr_images_upload', verbose_name='上传ID'),
        ),
    ]
