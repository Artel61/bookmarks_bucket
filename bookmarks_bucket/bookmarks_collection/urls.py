from django.urls import path, include


app_name = 'bookmarks'

urlpatterns = [
    path('', include('bookmarks_collection.api.urls')),
]
