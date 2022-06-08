from argparse import ArgumentTypeError
from datetime import date, datetime as dt
from operator import truediv
from os.path import abspath, exists
from urllib import error, request
try:
    from rapidjson import loads
except ImportError:
    from json import loads
from sxtools.logging import get_basic_logger
logger = get_basic_logger() # sXtools.log
from sxtools import __version__, __author__ as owner, __repository__ as repo

def apt_path_exists(path: str) -> str:
    '''
    Check if passed to <b>A</b>rgs<b>p</b>rser Directory exists
    :return: Path or ArgumentTypeError
    '''
    if exists(path):
        return abspath(path)
    else:
        raise ArgumentTypeError('No such file or directory')

def fview(s: str, sep: str='.') -> str: return s.replace(sep, ' ').title()
def bview(s: str, sep: str='.') -> str: return s.strip().replace(' ', sep).lower()

def strtdate(s: str) -> date:
    '''
    Convert a string to DATETIME and return its date part
    :return: DATE as "datetime.date" class
    '''
    for fmt in ('%Y-%m-%d', '%y.%m.%d', '%d-%m-%Y'):
        try:
            return dt.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f'No valid date format found in {s}')

def sortmap(d: dict) -> None:
    '''
    Sort a JSONfied dictionary by value
    '''
    for k, v in d.items():
        if type(v) == list: 
            v.sort()
        elif type(v) == dict: sortmap(v)

def check_updates() -> str:
    '''
    Check for Updates @ using GitHub API
    '''
    GITHUB_API_URL = 'https://api.github.com/repos/%s/%s/releases/latest'
    try:
        response = request.urlopen(
            GITHUB_API_URL % (owner, repo))
        version = loads(response.read()).get('tag_name').strip('v.')
    except error.HTTPError as e:
        logger.warning(f'{e} (check failed)')
        return 'no information, try later again'
    return 'latest' if version == __version__ else 'development build' if version < __version__ else 'outdated'

def table_readable(value: int) -> str:
    '''
    convert "value" in human readable format
    :return: "value" in next possible unit, e.g. 'KiB'
    '''
    try:
        if type(value) != int:
            value = int(value)
    except ValueError as e:
            logger.error(f'Couldn\'t convert "{value}" to an Integer')
            value = 0 # reset
    return f'{truediv(value, 1024 * 1024):0.1f} MiB'

def human_readable(value: int) -> str:
    '''
    convert "value" in human readable format
    :return: "value" in next possible unit, e.g. 'KiB'
    '''
    try:
        if type(value) != int:
            value = int(value)
    except ValueError as e:
            logger.error(f'Couldn\'t convert "{value}" to an Integer')
            value = 0 # reset
    for unit in ('bytes', 'KiB', 'MiB', 'GiB', 'TiB'):
        if value < 1024:
            return f'{value:0.2f} {unit}'
        value = truediv(value, 1024)
    return f'{value:0.1f} PiB' # pebibyte 1024^5 = 1,125,899,906,842,624 bytes
