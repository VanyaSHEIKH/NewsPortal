# Generated by Django 5.1 on 2024-09-05 22:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='date_in',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='category',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
