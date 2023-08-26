import base64
import hashlib

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models

from context import BookmarksCollectionController
from context.constants import OpenGraphMarkup


class LinkType(models.Model):
    """Тип ссылки на страницу"""

    cypher = models.CharField(verbose_name='Шифр', primary_key=True)
    description = models.CharField(verbose_name='Описание', null=False, default='')

    class Meta:
        verbose_name = 'Тип ссылки'
        verbose_name_plural = 'Типы ссылок'


class ModelManageMixin(models.Model):
    """Вспомогательные поля"""

    created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True, null=False)
    updated_at = models.DateTimeField(verbose_name='Изменена', auto_now=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BookmarkModelManager(models.Manager):
    """Менеджер моделей для закладок"""

    def make_bookmark_from_context(self, page_info: OpenGraphMarkup, user: User) -> 'Bookmark':
        preview = None

        if page_info.preview:
            split_chr = BookmarksCollectionController.img_info_splitter
            ext, raw_file = page_info.preview.split(split_chr)
            file_name = '.'.join([hashlib.md5(page_info.url.encode()).hexdigest(), ext.decode()])
            preview = ContentFile(base64.b64decode(raw_file), name=file_name)

        return Bookmark(
            user=user,
            page_title=page_info.title,
            short_description=page_info.description,
            page_url=page_info.url,
            page_type_id=page_info.page_type,
            preview=preview,
        )


class Bookmark(ModelManageMixin, models.Model):
    """Закладка страницы сайта"""

    page_title = models.CharField(verbose_name='Заголовок страницы', null=False, blank=False)
    short_description = models.TextField(verbose_name='Краткое описание', null=False, default='')
    page_url = models.URLField(verbose_name='Ссылка на страницу', null=False, blank=False)
    page_type = models.ForeignKey(LinkType, on_delete=models.DO_NOTHING, verbose_name='Тип ссылки', null=False)
    preview = models.ImageField(verbose_name='Картинка превью', upload_to='preview')

    objects = BookmarkModelManager()

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        unique_together = ('page_url', 'user')


class Collection(ModelManageMixin, models.Model):
    """Коллекции"""

    name = models.CharField(verbose_name='Название', null=False, unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', null=False, default='')
    bookmarks = models.ManyToManyField(Bookmark)

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
