# Generated by Django 4.0.4 on 2022-05-06 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=256)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.IntegerField(default=0)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=256)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]