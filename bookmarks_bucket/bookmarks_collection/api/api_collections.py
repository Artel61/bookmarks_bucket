from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookmarks_collection.models import Collection
from .serializers import CollectionSerializer


class CollectionsAPIViewSet(ModelViewSet):
    """Операции с коллекциями"""
    authentication_classes = [SessionAuthentication]
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.data
        data['user'] = self.request.user
        Collection.objects.create(**data)
