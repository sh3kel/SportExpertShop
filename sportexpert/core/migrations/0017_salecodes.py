# Generated by Django 4.2.1 on 2023-05-26 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_item_mainphoto_alter_item_photo1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
            ],
        ),
    ]
