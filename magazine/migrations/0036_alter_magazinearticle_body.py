# Generated by Django 3.2.7 on 2021-09-15 15:48

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0035_delete_magazineissuefeaturedarticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazinearticle',
            name='body',
            field=wagtail.core.fields.StreamField([('document', wagtail.documents.blocks.DocumentChooserBlock()), ('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'superscript', 'superscript', 'strikethrough', 'blockquote'])), ('pullquote', streams.blocks.PullQuoteBlock())]),
        ),
    ]