from datetime import date
from mimetypes import MimeTypes
from os.path import basename, getsize # posixpath
from re import IGNORECASE, sub
from subprocess import check_output
try:
    from rapidjson import loads  # extremely fast C++ JSON parser and serialization library
except ImportError:
    from json import loads
from sxtools.logging import get_basic_logger
logger = get_basic_logger()  # sXtools.log
from sxtools.utils import human_readable  # format


class Scene:

    def __init__(self, path: str) -> None:

        self.path, self.ext = path, path[-3:].lower()
        self.size = getsize(path)  # os.stat()
        self.performers = list()
        self.title, self.publisher = '', None
        self.released = date(1,1,1)
        self.ffprobed = False  # deep scan performed

    def __str__(self) -> str: return self.sanitize()

    def basename(self) -> str:
        '''
        return scene's basename using os.path
        '''
        return basename(self.path)

    def name(self) -> str:
        '''
        return scene's identification name
        '''
        return self.title or f'{self.perfs_as_string()} by {self.publisher}' if self.performers else '' or self.basename()

    def setTitle(self, title: str = '') -> None:
        '''
        set Title, remove multiple spaces and some other parts
        '''
        t = ' '.join((title or '').split())
        t = sub(' part (\d+)', ' (Part \g<1>)', t, flags=IGNORECASE)
        self.title = t

    def resolution(self) -> str:
        '''
        return scene's resolution
        '''
        return f'{self.w}x{self.h}' if self.ffprobed else 'not yet scanned'

    def perfs_as_string(self) -> str:
        '''
        return performers as a well-formed string
        '''
        return ', '.join(self.performers[:-2] + [' & '.join(self.performers[-2:])])

    def mimetype(self) -> str:
        '''
        return scene's mimetype, e.g. video-mp4
        '''
        return MimeTypes().guess_type(self.path)[0].replace(chr(47), chr(45))

    def sanitize(self) -> str:
        '''
        return sanitized scene's name as a string
        '''
        name = basename(self.path)[:-4] # .lower()
        sep = '.' if name.count('.') > name.count(' ') else ' '
        for ss in list(['[pt]']):
            name = name.replace(ss, sep)
        droplist = [
            '1080p', '1920p', '720p', '2160p',
            'bj', 'int', 'mp4',
            'mp4-gush', 'mp4-ktr', 'mp4-nbq', 'mp4-wrb',
            'repack', 'xxx' ]
        return sep.join(
            x for x in name.split(sep) if x and x.lower() not in droplist)

    def scan(self) -> None:
        '''
        read out video file's metadata using "ffprobe" (part of "ffmpeg")
        '''
        try:
            meta = loads(check_output(['ffprobe',
                    '-v', 'fatal',
                    '-select_streams',
                    'v:0',
                    '-show_entries',
                    'format=duration,bit_rate:stream=width,height',
                    '-of', 'json', self.path]))
            # get width & height of the scene
            self.h = meta['streams'][0]['height']
            self.w = meta['streams'][0]['width'] # v:0
            # get scene's bitrate
            self.bitrate = meta['format']['bit_rate']
            # get duration in seconds as float
            self.duration = meta['format']['duration']
            # check for suspicious resolutions
            if self.w != 1920: # 1080p
                logger.warning(f'Suspicious Resolution {self.resolution():^11} >  File: {self.basename()}')
            self.ffprobed = True
        except (FileNotFoundError) as e:
            logger.warning(f'No such file or directory: {e.filename}')

        # be sure "ffprobe" is installed, run "apt install ffmpeg" otherwise
