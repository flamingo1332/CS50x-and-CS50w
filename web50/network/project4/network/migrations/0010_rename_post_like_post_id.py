# Generated by Django 4.0.4 on 2022-05-09 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_comment_post_like_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='Post',
            new_name='Post_id',
        ),
    ]
