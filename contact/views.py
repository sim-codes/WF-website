from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.admin.viewsets.pages import PageListingViewSet
from memorials.views import MemorialViewSet
from .models import (
    Meeting,
    Organization,
    Person,
)


class PersonViewSet(PageListingViewSet):
    model = Person
    menu_label = "People"
    name = "people"
    icon = "user"
    search_fields = ["given_name", "family_name"]
    # Tried to add ordering to the columns, but it didn't work.
    # https://stackoverflow.com/questions/78563124/how-to-specify-ordering-for-wagtal-pagelistingviewset
    ordering = ["family_name", "given_name"]


class MeetingFilterSet(PageListingViewSet.filterset_class):
    class Meta:
        model = Meeting
        fields = [
            "meeting_type",
        ]


class MeetingViewSet(PageListingViewSet):
    model = Meeting
    menu_label = "Meetings"
    icon = "home"
    name = "meetings"
    search_fields = ["title"]
    filterset_class = MeetingFilterSet
    ordering = ["title"]


class OrganizationViewSet(PageListingViewSet):
    model = Organization
    menu_label = "Organizations"
    icon = "group"
    name = "organizations"
    search_fields = ["title"]
    ordering = ["title"]


class ContactViewSetGroup(ViewSetGroup):
    menu_label = "Contacts"
    menu_icon = "group"
    menu_order = 100
    items = [
        PersonViewSet,
        MeetingViewSet,
        OrganizationViewSet,
        MemorialViewSet,
    ]
