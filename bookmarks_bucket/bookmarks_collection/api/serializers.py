from rest_framework import serializers

from bookmarks_collection.models import Bookmark, Collection


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = (
            'bookmarks', 'user', 'created_at', 'updated_at',
        )


class CreateUserSerializer(serializers.Serializer):

    email = serializers.EmailField(allow_blank=False, allow_null=False, max_length=150)
    password = serializers.CharField(allow_null=False, allow_blank=False, max_length=100)


class OutputUserSerializer(serializers.Serializer):

    user_id = serializers.IntegerField(read_only=False)
    user_token = serializers.CharField(read_only=False)
