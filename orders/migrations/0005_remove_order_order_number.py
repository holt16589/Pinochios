# Generated by Django 2.1.5 on 2020-07-07 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200702_0332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
    ]
