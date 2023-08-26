from django.apps import AppConfig

from context.constants import EXTENDED_LINK_TYPES


class BookmarksCollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookmarks_collection'

    def ready(self):
        from .models import LinkType

        for link_type in LinkType.objects.all():
            EXTENDED_LINK_TYPES.add(link_type.cypher)
