from django.contrib import admin

from .models import Bookmark, Collection, LinkType


admin.site.register(LinkType)
admin.site.register(Collection)
admin.site.register(Bookmark)
