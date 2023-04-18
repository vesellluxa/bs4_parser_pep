# Проект парсинга pep
## Начало работы:
Склонируйте репозиторий. 
Это можно сделать командой :
`git clone https://github.com/vesellluxa/bs4_parser_pep.git`
Создайте виртуальное окружение:
`python -m venv venv`
Установите зависимости.
`pip install -r requirements.txt`
## Запуск парсера.
Зайдите в папку `src`.
`cd src`
## Запустите "main.py",  выбрав необходимый парсер и аргументы
`python main.py [парсер] [аргументы]`
## Парсеры:
### whats-new
Парсер, выводящий список изменений Python.
`python main.py whats-new [аргументы]`
### latest_versions
Парсер, выводящий список версий Python и ссылки на документацию.
`python main.py whats-new [аргументы]`
### download
Парсер,  скачивающий zip архив с документацией Python в PDF формате.
`python main.py whats-new [аргументы]`
### pep
Парсер,  выводящий статусы документов PEP и количество документов для каждого статуса.
`python main.py whats-new [аргументы]`
## Аргументы:
### -h, --help
Общая информация о командах.
`python main.py -h / --help`
### -c, --clear-cache
Очистка кеша перед выполнением парсинга.
`python main.py [парсер] -c / --clear-cache`
### -o {pretty, file}, --output {pretty, file}
Дополнительные способы вывода данных: 
pretty - выводит данные в командной строке в таблице.
file - сохраняет информацию в формате CSV в папке `./src/results/` .
`python main.py [парсер] -o pretty / file // -output pretty / file`
# Автор - [Алексей Шевич](https://github.com/vesellluxa)
# Стек:
## beautifulsoup4
## tqdm

