"""
Сервис для хранения ссылок пользователей.
"""
import base64
import requests

from .constants import LinkAttributes, OpenGraphMarkup
from .errors import NotFoundError, ResourceGettingError
from .parser import OpenGraphParser


class BookmarksCollectionController:
    """Контроллер для работы с закладками на страницы сайтов"""

    img_info_splitter = b';b64;'

    @classmethod
    def get_page_info_by_url(cls, url: str) -> OpenGraphMarkup:
        """Попытка получить веб страницу и определить разметку OpenGraph"""
        try:
            response = requests.get(url)
        except Exception:
            raise ResourceGettingError("Непредвиденная ошибка")

        if response.status_code == 404:
            raise NotFoundError()

        if response.status_code >= 500:
            raise ResourceGettingError("Непредвиденная ошибка")

        content = response.content.decode()
        prs = OpenGraphParser()
        prs.feed(content)
        markup = prs.opengraph_markup

        img_tag = LinkAttributes.IMAGE.value
        img_url = markup.get(img_tag)
        if img_url:
            image = cls.get_image_by_url(img_url)
            markup[img_tag] = image

        return OpenGraphMarkup.from_dict(prs.opengraph_markup)

    @classmethod
    def get_image_by_url(cls, url: str) -> bytes:
        """Попытка загрузить превью страницы"""
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_ext = url.split('.')[-1]
            raw_image = base64.b64encode(response.content)
            return cls.img_info_splitter.join([file_ext.encode(), raw_image])

        return b""
