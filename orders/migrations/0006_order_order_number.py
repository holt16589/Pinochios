# Generated by Django 2.1.5 on 2020-07-07 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=0),
        ),
    ]
