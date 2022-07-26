import logging  # ~/.config/sxtools/sXtools.log

from os.path import expanduser, join
from sys import stdout

PARSE = 14
REGEX = 15 # custom logging level, used for REGEX

def init_logging_config() -> None:
    '''
    Init 'basic' Configuration
    '''
    logging.basicConfig(
        datefmt='%d %b %H:%M:%S',
        # level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.StreamHandler(stdout), logging.FileHandler(join(expanduser('~/.config/sxtools'), 'SXTools.log'))])
    logging.addLevelName(REGEX, 'REGEX')
    logging.addLevelName(PARSE, 'PARSE')

def get_basic_logger() -> logging.Logger:
    '''
    Convenience Method to Load the App Logger
    :return: An Instance of the App Logger
    '''
    return logging.getLogger('Organizer!SXTools')
