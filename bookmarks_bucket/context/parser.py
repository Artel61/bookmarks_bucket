"""
Сервис для хранения ссылок пользователей.
Разбор ответа для выявления описания OpenGraph.
https://ogp.me/
"""
from html.parser import HTMLParser
from typing import Dict


class OpenGraphParser(HTMLParser):
    """Простой парсинг HTML страницы для определения OpenGraph тегов"""

    target = 'meta'
    property_name = 'property'
    content_name = 'content'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._meta_markup = dict()

    @property
    def opengraph_markup(self) -> Dict[str, str]:
        return self._meta_markup

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == self.target:
            prop, content = None, None
            for name, value in attrs:
                if name == self.property_name:
                    prop = value
                elif name == self.content_name:
                    content = value

            if prop and content:
                self._meta_markup[prop] = content
