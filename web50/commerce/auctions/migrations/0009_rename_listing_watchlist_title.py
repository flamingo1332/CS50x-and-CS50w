# Generated by Django 4.0.4 on 2022-04-28 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_listing_id_bids_listing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listing',
            new_name='title',
        ),
    ]
