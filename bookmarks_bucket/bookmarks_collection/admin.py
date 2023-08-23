from django.contrib import admin

from .models import Collection, LinkType


admin.site.register(LinkType)
admin.site.register(Collection)
