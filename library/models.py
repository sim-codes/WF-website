from django.db import models
from django.http import HttpRequest
from django_flatpickr.widgets import DatePickerInput
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail import blocks as wagtail_blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from blocks.blocks import (
    FormattedImageChooserStructBlock,
    HeadingBlock,
    MediaBlock,
    PullQuoteBlock,
    SpacerBlock,
    WfURLBlock,
)
from common.models import DrupalFields
from documents.blocks import DocumentEmbedBlock
from facets.models import Audience, Genre, Medium, TimePeriod, Topic
from pagination.helpers import get_paginated_items


class LibraryItemTag(TaggedItemBase):
    content_object = ParentalKey(
        to="LibraryItem",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class LibraryItem(DrupalFields, Page):
    publication_date = models.DateField("Publication date", null=True, blank=True)
    publication_date_is_approximate = models.BooleanField(
        default=False,
        help_text="This field indicates when a library item wasn't published on a specific publication date.",  # noqa: E501
    )
    body = StreamField(
        [
            ("heading", HeadingBlock()),
            (
                "rich_text",
                wagtail_blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "link",
                        "hr",
                    ],
                ),
            ),
            (
                "image",
                FormattedImageChooserStructBlock(
                    classname="full title",
                ),
            ),
            ("document", DocumentEmbedBlock()),
            (
                "media",
                MediaBlock(
                    icon="media",
                ),
            ),
            ("embed", EmbedBlock()),
            ("url", WfURLBlock()),
            ("pullquote", PullQuoteBlock()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    item_audience = models.ForeignKey(
        "facets.Audience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    item_genre = models.ForeignKey(
        "facets.Genre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    item_medium = models.ForeignKey(
        "facets.Medium",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    item_time_period = models.ForeignKey(
        "facets.TimePeriod",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tags = ClusterTaggableManager(
        through=LibraryItemTag,
        blank=True,
    )

    content_panels = Page.content_panels + [
        InlinePanel(
            "authors",
            heading="Authors",
            help_text="Select one or more authors, who contributed to this article",
        ),
        FieldPanel("body"),
        MultiFieldPanel(
            children=[
                FieldPanel(
                    "publication_date",
                    widget=DatePickerInput(),
                ),
                FieldPanel(
                    "publication_date_is_approximate",
                ),
            ],
            heading="Publication date",
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("item_audience"),
                FieldPanel("item_genre"),
                FieldPanel("item_medium"),
                FieldPanel("item_time_period"),
                InlinePanel(
                    "topics",
                    label="topics",
                ),
                FieldPanel("tags"),
            ],
            heading="Categorization",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.RelatedFields(
            "item_genre",
            [
                index.SearchField("title"),
            ],
        ),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name"),
            ],
        ),
        index.RelatedFields(
            "topics",
            [
                index.SearchField("topic"),
            ],
        ),
    ]

    parent_page_types = ["LibraryIndexPage"]
    subpage_types: list[str] = []


class LibraryItemAuthor(Orderable):
    library_item = ParentalKey(
        "library.LibraryItem",
        null=True,
        on_delete=models.CASCADE,
        related_name="authors",
    )
    author = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.CASCADE,
        related_name="library_items_authored",
    )

    panels = [
        PageChooserPanel(
            "author",
            [
                "contact.Person",
                "contact.Meeting",
                "contact.Organization",
            ],
        ),
    ]


class LibraryItemTopic(Orderable):
    library_item = ParentalKey(
        "library.LibraryItem",
        null=True,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    topic = models.ForeignKey(
        "facets.Topic",
        null=True,
        on_delete=models.CASCADE,
        related_name="related_library_items",
    )

    panels = [
        PageChooserPanel(
            "topic",
        ),
    ]


class LibraryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ["home.HomePage"]
    subpage_types: list[str] = [
        "library.LibraryItem",
        "facets.FacetIndexPage",
    ]

    max_count = 1

    def get_context(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        context = super().get_context(request)

        # Prepare a list of authors
        library_item_authors = LibraryItemAuthor.objects.all()
        authors = Page.objects.filter(
            library_items_authored__in=library_item_authors,
        ).distinct()

        # Populate faceted search fields
        context["audiences"] = Audience.objects.all()
        context["genres"] = Genre.objects.all()
        context["mediums"] = Medium.objects.all()
        context["time_periods"] = TimePeriod.objects.all()
        context["topics"] = Topic.objects.all()
        context["authors"] = authors

        query = request.GET.dict()

        # Define allow keys that are model fields
        allowed_keys = [
            "authors__author__title",
            "item_audience__title",
            "item_genre__title",
            "item_medium__title",
            "item_time_period__title",
            "title__icontains",
            "topics__topic__title",
        ]

        # Remove any query parameter that
        # - isn't a model field, or
        # - has an empty value (empty string)
        facets = {
            key: value
            for key, value in query.items()
            if key in allowed_keys and value != ""
        }

        # Filter live (not draft) library items using facets from request
        library_items = LibraryItem.objects.live().filter(
            **facets,
        )
        page_number = request.GET.get("page", "1")
        items_per_page = 10

        # Provide filtered, paginated library items
        context["paginated_items"] = get_paginated_items(
            items=library_items,
            items_per_page=items_per_page,
            page_number=page_number,
        )

        context["current_querystring"] = "&".join(
            f"{key}={value}" for key, value in facets.items()
        )

        return context
