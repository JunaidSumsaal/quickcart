# Generated by Django 4.2.20 on 2025-03-13 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_ordertracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
