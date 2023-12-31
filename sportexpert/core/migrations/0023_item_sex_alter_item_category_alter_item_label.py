# Generated by Django 4.2.1 on 2023-05-26 11:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_coupon_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sex',
            field=models.CharField(choices=[('M', 'Мужское'), ('W', 'Женское'), ('MK', 'Мальчик'), ('WK', 'Девочка'), ('U', 'Унисекс')], default=django.utils.timezone.now, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('K', 'Кеды'), ('KR', 'Кроссовки'), ('BT', 'Ботинки'), ('AC', 'Аксессуары')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'Новое'), ('S', 'Распродажа'), ('D', 'Хит')], max_length=1),
        ),
    ]
