# Generated by Django 3.0.8 on 2020-08-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comments_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('list_id', models.IntegerField()),
                ('bid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=64)),
                ('winner', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('winprice', models.IntegerField()),
                ('title', models.CharField(max_length=64, null=True)),
            ],
        ),
    ]