# Generated by Django 3.0.8 on 2020-07-31 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='auctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('seller_username', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starting_bid', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.URLField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
