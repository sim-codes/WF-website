# Generated by Django 4.2.1 on 2023-06-21 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("donations", "0001_squashed_0002_alter_donatepage_suggested_donation_amounts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donoraddress",
            name="country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]