# Generated by Django 2.1 on 2019-11-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_articlepost_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='total_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]