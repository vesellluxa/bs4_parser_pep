import logging

from bs4 import BeautifulSoup
from requests import RequestException

from constants import BEAUTIFUL_SOUP_FEATURE_ARGUMENT
from exceptions import ParserFindTagException


EMPTY_RESPONSE_MESSAGE = 'Ответ от {url} не получен.'

REQUEST_EXCEPTION_MESSAGE = 'Ошибка при загрузке страницы! {url}'

NOT_FOUND_TAG_MESSAGE = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        if response is None:
            raise ValueError(
                EMPTY_RESPONSE_MESSAGE.format(url=url)
            )
        return response
    except RequestException:
        raise ValueError(
            REQUEST_EXCEPTION_MESSAGE.format(url=url),
        )


def create_soup(session, url):
    return BeautifulSoup(get_response(session, url).text, features=BEAUTIFUL_SOUP_FEATURE_ARGUMENT)


def find_tag(soup, tag, attrs=None):
    tag_to_search = soup.find(tag, attrs=(attrs or {}))
    if tag_to_search is None:
        error_message = NOT_FOUND_TAG_MESSAGE.format(
            tag=tag,
            attrs=attrs
        )
        logging.error(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return tag_to_search
