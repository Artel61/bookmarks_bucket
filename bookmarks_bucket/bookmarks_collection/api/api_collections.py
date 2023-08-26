from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from bookmarks_collection.models import Collection

from .authentication import CustomTokenAuthentication
from .serializers import CollectionSerializer


class CollectionsAPIViewSet(ModelViewSet):
    """Операции с коллекциями"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.data
        data['user'] = self.request.user
        Collection.objects.create(**data)
