# Generated by Django 4.2.1 on 2023-05-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_item_category_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test_product'),
            preserve_default=False,
        ),
    ]
