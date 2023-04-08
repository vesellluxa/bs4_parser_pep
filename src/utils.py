import logging

from requests import RequestException

from exceptions import ParserFindTagException, EmptyResponseException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        if response is None:
            raise EmptyResponseException(f'Ответ от {url} не получен.')
        return response
    except RequestException:
        logging.exception(
            f'Ошибка при загрузке страницы! {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    tag_to_search = soup.find(tag, attrs=(attrs or {}))
    if tag_to_search is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return tag_to_search
