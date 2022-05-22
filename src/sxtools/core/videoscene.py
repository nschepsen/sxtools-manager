
from os.path import basename, getsize  # posixpath
from subprocess import CalledProcessError, check_output

from rapidjson import loads # extremely fast C++ JSON parser and serialization library

from sxtools.logging import get_basic_logger
logger = get_basic_logger() # sXtools.log
from sxtools.utils import human_readable  # format


class Scene:

    performers, publisher, released, title = list(), '', '', ''

    def __init__(self, path: str, scan: bool=True) -> None:

        self.path, self.ext = path, path[-3:].lower()
        self.size = getsize(path) # os.stat()
        self.scanned = scan # deep scan performed
        # read out the scene's metadata with ffprobe
        if not scan:
            return
        # be sure "ffprobe" is installed, run "apt install ffmpeg" otherwise
        try:
            meta = loads(
                check_output(['ffprobe',
                    '-v', 'fatal',
                    '-select_streams',
                    'v:0',
                    '-show_entries',
                    'format=duration,bit_rate:stream=width,height',
                    '-of', 'json', path]))
            # get width & height of the scene
            self.h = meta['streams'][0]['height']
            self.w = meta['streams'][0]['width'] # v:0
            # get scene's bitrate
            self.bitrate = meta['format']['bit_rate']
            # get duration in seconds as float
            self.duration = meta['format']['duration']
            # check for suspicious resolutions
            if self.w != 1920: # 1080p
                logger.warning(
                    f'Suspicious Resolution {self.resolution():^11}'
                    f' >  File: {basename(path)}')
        except (FileNotFoundError) as e:
            logger.warning(f'No such file or directory: {e.filename}')

    def __str__(self) -> str: return self.sanitized()

    def resolution(self) -> str:
        '''
        return scene resolution
        '''
        return f'{self.w}x{self.h}' if self.scanned else 'no scans performed'

    def perfs_as_string(self) -> str:
        '''
        return performers as a well-formed string
        '''
        return ', '.join(self.performers[:-2] + [' & '.join(self.performers[-2:])])

    def sanitized(self) -> str:
        '''
        return the scene name sanitized as a string
        '''
        name = basename(self.path)[:-4] # .lower()
        for ss in list(['[pt]']):
            name = name.replace(ss, '.')
        droplist = [
            '1080p', '1920p', '720p', '2160p',
            'bj', 'int', 'mp4',
            'mp4-gush', 'mp4-ktr', 'mp4-nbq', 'mp4-wrb',
            'repack', 'xxx' ]
        return '.'.join(
            filter(
                lambda x: x and x.lower() not in droplist, ' '.join(name.split()).split('.')))
