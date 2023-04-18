from pathlib import Path
from urllib.parse import urljoin

BEAUTIFUL_SOUP_FEATURE_ARGUMENT = 'lxml'

PRETTY_OUTPUT_CONSTANT = 'pretty'

FILE_OUTPUT_CONSTANT = 'file'

BASE_DIR = Path(__file__).parent

DOWNLOADS = 'downloads'

RESULTS = 'results'

LOG_DIR = BASE_DIR / 'logs'

LOG_FILE = LOG_DIR / 'parser.log'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}


LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DT_LOG_FORMAT = '%d.%m.%Y %H:%M:%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'

PEP_LIST_URL = 'https://peps.python.org/'

DOWNLOAD_URL = urljoin(MAIN_DOC_URL, 'download.html')
