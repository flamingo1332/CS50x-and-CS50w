# Generated by Django 4.0.4 on 2022-05-09 10:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_rename_post_like_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liker',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), default=list, size=None),
        ),
    ]
