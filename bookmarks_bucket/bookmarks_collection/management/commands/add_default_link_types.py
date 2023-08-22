from django.core.management.base import BaseCommand


from bookmarks_collection.models import LinkType
from context.constants import BASE_LINK_DESCRIPTIONS, BaseLinkTypes


class Command(BaseCommand):
    help = "Adds default content types if they are not exists"

    def handle(self, *args, **options):
        self.stdout.write(self.help)

        for link_type in BaseLinkTypes:
            obj, _ = LinkType.objects.get_or_create(
                cypher=link_type.value,
                description=BASE_LINK_DESCRIPTIONS[link_type],
                defaults={'description': BASE_LINK_DESCRIPTIONS[link_type]},
            )

        self.stdout.write(
            self.style.SUCCESS('Done')
        )
