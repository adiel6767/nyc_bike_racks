# Generated by Django 5.0.6 on 2024-11-14 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_parking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikerackdata',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]