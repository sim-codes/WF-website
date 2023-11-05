# Generated by Django 4.2.5 on 2023-10-18 16:25

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0015_alter_subscription_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriptionindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                    (
                        "paypal_button",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "paypal_plan_id",
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                                (
                                    "paypal_plan_name",
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                                (
                                    "paypal_plan_price",
                                    wagtail.blocks.IntegerBlock(required=True),
                                ),
                            ]
                        ),
                    ),
                    (
                        "card_row",
                        wagtail.blocks.ListBlock(
                            wagtail.blocks.StructBlock(
                                [
                                    (
                                        "paypal_plan_id",
                                        wagtail.blocks.CharBlock(required=True),
                                    ),
                                    (
                                        "paypal_plan_name",
                                        wagtail.blocks.CharBlock(required=True),
                                    ),
                                    (
                                        "paypal_plan_price",
                                        wagtail.blocks.IntegerBlock(required=True),
                                    ),
                                ]
                            ),
                            template="blocks/blocks/card_row.html",
                        ),
                    ),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]
