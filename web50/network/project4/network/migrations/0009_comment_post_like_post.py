# Generated by Django 4.0.4 on 2022-05-09 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_like_liker'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='Post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commented_post', to='network.post'),
        ),
        migrations.AddField(
            model_name='like',
            name='Post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_post', to='network.post'),
        ),
    ]
