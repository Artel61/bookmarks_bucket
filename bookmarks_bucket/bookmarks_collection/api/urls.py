from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_bookmarks import BookmarkAPIActions, BookmarkAPIViewSet


router = DefaultRouter()
router.register('bookmark', BookmarkAPIViewSet, basename='bookmarks')
router.register('bookmark/actions', BookmarkAPIActions, basename='bookmarks-actions')

# TODO: - Зарегистрироваться.Регистрация по email и паролю
#       - Войти / Выйти из системы
#       - Добавить коллекцию
#       - Удалить коллекцию(Удаляется только коллекция, закладки остаются у пользователя)
#       - Поменять название / описание коллекции

urlpatterns = [
    path('', include(router.urls)),
]
