# Generated by Django 4.2.1 on 2023-05-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_coupon_alter_order_code_delete_salecodes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='code',
            new_name='coupon',
        ),
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]