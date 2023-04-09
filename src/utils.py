import logging

from requests import RequestException

from exceptions import ParserFindTagException, EmptyResponseException

EMPTY_RESPONSE_MESSAGE = 'Ответ от {url} не получен.'

REQUEST_EXCEPTION_MESSAGE = 'Ошибка при загрузке страницы! {url}'

NOT_FOUND_TAG_MESSAGE = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        if response is None:
            raise EmptyResponseException(
                EMPTY_RESPONSE_MESSAGE.format(url=url)
            )
        return response
    except RequestException:
        logging.exception(
            REQUEST_EXCEPTION_MESSAGE.format(url=url),
            stack_info=True
        )


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
