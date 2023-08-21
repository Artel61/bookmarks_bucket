from django.db import models


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

    class Meta:
        abstract = True


class Bookmark(ModelManageMixin, models.Model):
    """Закладка страницы сайта"""

    page_title = models.CharField(verbose_name='Заголовок страницы', null=False, blank=False)
    short_description = models.TextField(verbose_name='Краткое описание', null=False, default='')
    page_url = models.URLField(verbose_name='Ссылка на страницу', null=False, blank=False, unique=True)
    page_type = models.ForeignKey(LinkType, on_delete=models.DO_NOTHING, verbose_name='Тип ссылки', null=False)
    preview = models.ImageField(verbose_name='Картинка превью')

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'


class Collection(ModelManageMixin, models.Model):
    """Коллекции"""

    name = models.CharField(verbose_name='Название', null=False, unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', null=False, default='')
    bookmarks = models.ManyToManyField(Bookmark)

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
