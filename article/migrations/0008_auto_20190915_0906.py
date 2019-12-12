# Generated by Django 2.1 on 2019-09-15 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20190910_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='body',
            field=mdeditor.fields.MDTextField(verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='title',
            field=models.CharField(max_length=100, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
