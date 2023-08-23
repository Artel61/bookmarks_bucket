"""
Сервис для хранения ссылок пользователей.
Константы, перечисления, дата-классы.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from .errors import UnknownTypeError


class LinkAttributes(Enum):
    TITLE = 'og:title'
    DESCRIPTION = 'og:description'
    TYPE = 'og:type'
    IMAGE = 'og:image'
    URL = 'og:url'


class BaseLinkTypes(Enum):
    WEBSITE = 'website'
    BOOK = 'book'
    ARTICLE = 'article'
    MUSIC = 'music'
    VIDEO = 'video'


BASE_LINK_DESCRIPTIONS = {
    BaseLinkTypes.WEBSITE: 'Веб сайт',
    BaseLinkTypes.BOOK: 'Книга',
    BaseLinkTypes.ARTICLE: 'Статья',
    BaseLinkTypes.MUSIC: 'Аудио',
    BaseLinkTypes.VIDEO: 'Видео',
}

DEFAULT_LINK_TYPE = BaseLinkTypes.WEBSITE
# NOTE: согласно постановке задачи, список типов может быть расширен
EXTENDED_LINK_TYPES = {t.value for t in BaseLinkTypes}


@dataclass
class OpenGraphMarkup:

    page_type: str
    title: Optional[str] = ''
    description: Optional[str] = ''
    url: Optional[str] = ''
    preview: Optional[str] = None

    @classmethod
    def from_fict(cls, data: Dict[str, str]) -> 'OpenGraphMarkup':
        content_type = data.get(LinkAttributes.TYPE.value) or DEFAULT_LINK_TYPE.value

        if content_type not in EXTENDED_LINK_TYPES:
            raise UnknownTypeError()

        return cls(
            page_type=content_type,
            title=data.get(LinkAttributes.TITLE.value, ''),
            description=data.get(LinkAttributes.DESCRIPTION.value, ''),
            url=data.get(LinkAttributes.URL.value, ''),
            preview=data.get(LinkAttributes.IMAGE.value, '')
        )
