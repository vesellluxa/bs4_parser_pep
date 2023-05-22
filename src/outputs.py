import csv
import datetime as dt
import logging

from csv import unix_dialect
from prettytable import PrettyTable

from constants import (BASE_DIR, DATETIME_FORMAT,
                       PRETTY_OUTPUT, FILE_OUTPUT, RESULTS)
from exceptions import PrintException

FILE_OUTPUT_LOGGING = 'CSV файл с результатами сохранён по адресу: {file_path}'

PRETTY_OUTPUT_LOGGING_ERROR = 'Ошибка вывода: {error}'


def file_output(results, cli_args, encoding='utf-8'):
    results_dir = BASE_DIR / RESULTS
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding=encoding) as file:
        writer = csv.writer(file, dialect=unix_dialect)
        writer.writerows(results)

    logging.info(FILE_OUTPUT_LOGGING.format(file_path=file_path))


def pretty_output(results, cli_args):
    try:
        table = PrettyTable()
        table.field_names = results[0]
        table.align = 'l'
        table.add_rows(results[1:])
        print(table)
    except PrintException as error:
        logging.error(
            PRETTY_OUTPUT_LOGGING_ERROR.format(error=error)
        )


def default_output(results, cli_args):
    for row in results:
        print(*row)


OUTPUTS = {
    PRETTY_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    None: default_output
}


def control_output(results, cli_args):
    OUTPUTS[cli_args.output](results, cli_args)
