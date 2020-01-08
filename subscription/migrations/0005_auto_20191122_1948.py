# Generated by Django 2.2.4 on 2019-11-22 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_subscriptionindexpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='subscriber_address_country',
            field=models.CharField(blank=True, default='United States', help_text='Country for shipping.', max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber_address_locality',
            field=models.CharField(blank=True, help_text='City for the shipping address.', max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber_family_name',
            field=models.CharField(default='', help_text='Enter the family name for the subscriber.', max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber_given_name',
            field=models.CharField(default='', help_text='Enter the given name for the subscriber.', max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber_postal_code',
            field=models.CharField(blank=True, help_text='Postal code for the shipping address.', max_length=16),
        ),
    ]