import logging
import re
import requests_cache

from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_LIST_URL,
                       DOWNLOAD_URL, DOWNLOADS)
from exceptions import NothingFoundException, FailedSoupCreationException
from outputs import control_output
from utils import find_tag, create_soup

PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
URL_REGEX = re.compile(r'.+pdf-a4\.zip$')
NOTHING_FOUND_EXCEPTION_INFO = 'Ничего не найдено!'
DOWNLOAD_LOGGING_INFO = 'Архив сохранён: {archive_path}'
PEP_LOGGING_INFO = ('\nНекорректный статус в общем списке: {short_status}\n'
                    'Строка PEP: {pep_line}')
NO_STATUS_LOGGING_INFO = 'Не найдена строка статуса! {pep_line_link}'
STATUS_MISMATCH_LOGGING_INFO = ('\nНесовпадение статусов:\n'
                                '{pep_line_link}\n'
                                'Статус в карточке - {status_num}\n'
                                'Ожидаемые статусы - {status_ext}')
SUM_MISMATCH_LOGGING_INFO = ('\n Ошибка в сумме:\n'
                             'Всего PEP: {pep_count}'
                             'Статусов из карточек: {status_counter}')
PARSER_START_LOGGING_INFO = 'Парсер запущен!'
PARSER_START_ARGS_LOGGING_INFO = 'Аргументы при запуске: {args}'
PARSER_COMPLETED_WORK = 'Парсер завершил работу!'
FAILED_CREATE_SOUP_INFO = 'Не удалось создать SOUP! {url}, {error}'
PARSER_WORK_ERROR = ('Во время выполнения работы парсера'
                     ' произошла ошибка! {error}')


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = create_soup(session, whats_new_url)
    main_div = find_tag(
        soup,
        'section',
        attrs={'id': 'what-s-new-in-python'}
    )
    div_ul = find_tag(
        main_div,
        'div',
        attrs={'class': 'toctree-wrapper'}
    )
    sections_by_python = div_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    exceptions = []
    for section in tqdm(sections_by_python):
        a_tag = section.find('a')
        href = a_tag['href']
        link = urljoin(whats_new_url, href)
        try:
            soup = create_soup(session, link)
        except Exception as error:
            exceptions.append(FailedSoupCreationException(
                FAILED_CREATE_SOUP_INFO.format(
                    url=MAIN_DOC_URL,
                    error=error
                )
            ))
        h1_tag = find_tag(soup, 'h1')
        dl_tag = find_tag(soup, 'dl')
        dl_text = dl_tag.text.replace('\n', ' ')
        results.append((link, h1_tag.text, dl_text))
    for exception in exceptions:
        logging.info(exception)
    return results


def latest_versions(session):
    soup = create_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(
        soup,
        'div',
        attrs={'class': 'sphinxsidebarwrapper'}
    )
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise NothingFoundException(NOTHING_FOUND_EXCEPTION_INFO)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    for a_tag in tqdm(a_tags):
        link = a_tag['href']
        text_match = re.search(PATTERN, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    soup = create_soup(session, DOWNLOAD_URL)
    link_table = find_tag(soup, 'table')
    pdf_a4_tag = find_tag(
        link_table,
        'a',
        attrs={'href': URL_REGEX}
    )
    archive_url = urljoin(DOWNLOAD_URL, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(
        DOWNLOAD_LOGGING_INFO.format(archive_path=archive_path)
    )


def pep(session):
    soup = create_soup(session, PEP_LIST_URL)
    index = find_tag(
        soup,
        'section',
        attrs={'id': 'numerical-index'}
    )
    pep_list = find_tag(index, 'tbody')
    pep_lines = pep_list.find_all('tr')
    pep_count, status_counter = 0, 0
    results = [('Статус', 'Количество')]
    exceptions = []
    for pep_line in tqdm(pep_lines):
        pep_count += 1
        short_status = pep_line.find('td').text[1:]
        try:
            status_ext = EXPECTED_STATUS[short_status]
        except KeyError:
            status_ext = []
            exceptions.append(ValueError(
                PEP_LOGGING_INFO.format(short_status=short_status,
                                        pep_line=pep_line)
            ))
        link = find_tag(pep_line, 'a')['href']
        pep_line_link = urljoin(PEP_LIST_URL, link)
        try:
            soup = create_soup(session, pep_line_link)
        except Exception as error:
            exceptions.append(ValueError(
                FAILED_CREATE_SOUP_INFO.format(
                    url=MAIN_DOC_URL,
                    error=error
                )))
        dl_tag = find_tag(soup, 'dl')
        status = dl_tag.find(string='Status')
        if not status:
            exceptions.append(ValueError(NO_STATUS_LOGGING_INFO.format(
                pep_line_link=pep_line_link
            )))
        status = status.find_parent()
        status_num = status.next_sibling.next_sibling.string
        if status_num not in status_ext:
            exceptions.append(ValueError(
                STATUS_MISMATCH_LOGGING_INFO.format(
                    pep_line_link=pep_line_link,
                    status_num=status_num,
                    status_ext=status_ext
                )
            ))
        status_counter += 1
    for exception in exceptions:
        logging.info(exception)
    if pep_count != status_counter:
        logging.error(
            f'\n Ошибка в сумме:\n'
            f'Всего PEP: {pep_count}'
            f'Статусов из карточек: {status_counter}'
        )
        results.append(('Total', status_counter))
    else:
        results.append(('Всего', pep_count))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(PARSER_START_LOGGING_INFO)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(PARSER_START_ARGS_LOGGING_INFO.format(
        args=args
    ))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.info(
            PARSER_WORK_ERROR.format(
                error=error
            )
        )
    logging.info(PARSER_COMPLETED_WORK)


if __name__ == "__main__":
    main()
