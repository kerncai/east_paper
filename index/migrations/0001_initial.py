# Generated by Django 2.0.6 on 2018-06-13 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, null=True, verbose_name='登录用户')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='用户地址')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
            ],
            options={
                'verbose_name': '平台登录',
                'db_table': 'LoginLogs',
                'verbose_name_plural': '平台登录',
            },
        ),
    ]
