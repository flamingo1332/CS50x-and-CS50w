# Generated by Django 4.0.4 on 2022-04-28 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_listing_watchlist_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='title',
            new_name='listing',
        ),
    ]