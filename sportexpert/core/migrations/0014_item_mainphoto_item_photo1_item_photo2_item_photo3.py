# Generated by Django 4.2.1 on 2023-05-25 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_postaddress_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mainPhoto',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
