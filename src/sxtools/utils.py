from argparse import ArgumentTypeError
from datetime import date, datetime as dt
from hashlib import md5
from operator import truediv
from os import makedirs, scandir, unlink
from os.path import abspath, exists, expanduser, join
from typing import Union
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
    for fmt in ('%Y-%m-%d', '%y.%m.%d', '%d-%m-%Y', '%m.%d.%y'):
        try:
            return dt.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f'No valid date format found in {s}')

def sortmap(d: dict) -> None:
    '''
    Sort a JSONfied dictionary by value
    '''
    for v in d.values():
        if type(v) == list:
            v.sort()
        elif type(v) == dict: sortmap(v)

def cache(object: str = None, init: bool = False) -> Union[str, bool]:
    '''
    Return the app's cache directory or path to a object in the cache
    '''
    d = expanduser('~/.config/sxtools/cache')
    if not exists(d): # check if cache exists
        makedirs(d, exist_ok=True)
    if not object:
        return d # return cache directory
    path = join(
        d, md5(object.encode('utf-8')).hexdigest() + '.jpg')
    return path if exists(path) or init else False # Union[path | False]

def cache_size() -> int:
    '''
    Calculate the size of cache directory
    '''
    total = 0
    with scandir(cache()) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += cache_size(entry.path)
    return total

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
    return 'latest' if version == __version__ else 'development' if version < __version__ else 'outdated'

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
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if value < 1024:
            return f'{value:0.2f} {unit}'
        value = truediv(value, 1024)
    return f'{value:0.1f} PiB' # pebibyte 1024^5 = 1,125,899,906,842,624 bytes
