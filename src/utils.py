from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


EMPTY_RESPONSE_MESSAGE = 'Ответ от {url} не получен.'
REQUEST_EXCEPTION_MESSAGE = 'Ошибка при загрузке страницы! {url}, {error}'
NOT_FOUND_TAG_MESSAGE = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        if response is None:
            raise Exception(
                EMPTY_RESPONSE_MESSAGE.format(url=url)
            )
        return response
    except RequestException as error:
        raise Exception(
            REQUEST_EXCEPTION_MESSAGE.format(url=url, error=error),
        )


def create_soup(session, url, features='lxml'):
    try:
        return BeautifulSoup(
            get_response(session, url).text,
            features=features
        )
    except Exception as error:
        raise Exception(error)


def find_tag(soup, tag, attrs=None):
    tag_to_search = soup.find(tag, attrs=(attrs or {}))
    if tag_to_search is None:
        error_message = NOT_FOUND_TAG_MESSAGE.format(
            tag=tag,
            attrs=attrs
        )
        raise ParserFindTagException(error_message)
    return tag_to_search
