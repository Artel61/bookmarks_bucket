from typing import Optional

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet

from bookmarks_collection.models import Bookmark, Collection

from context import BookmarksCollectionController
from context.constants import OpenGraphMarkup
from context.errors import CustomError, NotFoundError

from .serializers import BookmarkSerializer


controller = BookmarksCollectionController()

input_url_param = openapi.Schema(
    title='url',
    description='URL для добавления в закладки',
    type=openapi.TYPE_STRING,
)
input_collection_param = openapi.Schema(
    title='collection',
    description='Идентификатор коллекции',
    type=openapi.TYPE_INTEGER,
)

output_param = openapi.Response('Ответ', BookmarkSerializer)
error_response = openapi.Response(
    'Описание ошибки',
    openapi.Schema(
        'data',
        description='Строка с описанием ошибки',
        type=openapi.TYPE_STRING,
    ),
)

post_response_map = {
    status.HTTP_200_OK: output_param,
    status.HTTP_400_BAD_REQUEST: error_response,
    status.HTTP_404_NOT_FOUND: error_response,
    status.HTTP_422_UNPROCESSABLE_ENTITY: error_response,
}
put_response_map = {
    status.HTTP_200_OK: None,
    status.HTTP_400_BAD_REQUEST: error_response,
    status.HTTP_404_NOT_FOUND: error_response,
    status.HTTP_403_FORBIDDEN: error_response,
}


class BookmarkAPIViewSet(ReadOnlyModelViewSet):
    """Просмотр закладок"""
    authentication_classes = [SessionAuthentication]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BookmarkAPIActions(ViewSet):
    """Операции с закладками"""

    def get_object(self, pk) -> Optional[Bookmark]:
        return Bookmark.objects.filter(id=pk).first()

    @swagger_auto_schema(method='POST', request_body=input_url_param, responses=post_response_map)
    @action(methods=['POST'], detail=False)
    def add_bookmark(self, request: Request) -> Response:
        """Добавление закладки"""
        req_data = request.data
        url = req_data.get('url')

        if not url:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Ожидалась URL строка')

        same_url = Bookmark.objects.filter(page_url=url).first()
        if same_url:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Закладка с таким URL уже существует')

        try:
            page_info: OpenGraphMarkup = controller.get_page_info_by_url(url)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND, data='URL не найден')
        except CustomError:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        new_bookmark = Bookmark.objects.make_bookmark_from_context(page_info, request.user)
        new_bookmark.save()

        return Response(BookmarkSerializer(instance=new_bookmark).data)

    @action(methods=['DELETE'], detail=True)
    def delete_bookmark(self, request: Request, pk=None) -> Response:
        """Удаление закладки"""
        bookmark = self.get_object(pk)

        if not bookmark:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Закладки не существует')

        if bookmark.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data='Нельзя удалять чужие закладки')

        bookmark.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(method='PUT', request_body=input_collection_param, responses=put_response_map)
    @action(methods=['PUT'], detail=True)
    def add_bookmark_to_collection(self, request: Request, pk=None) -> Response:
        """Добавить закладку в коллекцию"""
        req_data = request.data
        id_collection = req_data.get('collection')

        bookmark = self.get_object(pk)
        if not bookmark:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Закладки не существует')

        if bookmark.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data='Нельзя брать чужие закладки')

        collection = Collection.objects.filter(pk=id_collection).first()
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Коллекции не существует')

        if collection.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data='Нельзя подсовывать людям чужие закладки')

        if collection.filter(bookmarks__id=bookmark.pk).first():
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Закладка уже в коллекции')

        collection.bookmarks.add(bookmark)
        return Response(status=status.HTTP_200_OK)
