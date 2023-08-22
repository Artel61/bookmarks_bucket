from enum import Enum


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
