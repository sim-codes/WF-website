# Generated by Django 5.0.6 on 2024-05-29 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_remove_order_recipient_po_box_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
