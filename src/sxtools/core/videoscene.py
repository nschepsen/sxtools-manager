# from datetime import date  # released min date(1, 1, 1)
from mimetypes import MimeTypes
from os.path import basename, getsize  # posixpath
from random import randrange
from re import IGNORECASE, sub
from subprocess import call, check_output
# extremely fast C++ JSON parser and serialization library
from rapidjson import loads
from sxtools.logging import get_basic_logger
logger = get_basic_logger()  # sXtools.log
from sxtools.utils import cache  # keep thumbnails in one place


class Scene:

    def __init__(self, path: str) -> None:

        self.path, self.ext = path, path[-3:].lower()
        self.size = getsize(path) # os.stat()
        self.performers = list()
        self.title, self.paysite = '', ''
        self.released = None # not set yet | date.min
        self.ffprobed = False # get metadata using ffprobe, e.g. bitrate, resolution, duration

    def __str__(self) -> str:

        return self.sanitize()

    def is_valid(self) -> bool:
        '''
        check if scene well-parsed is
        '''
        return bool(self.released and self.performers and self.paysite)

    def basename(self) -> str:
        '''
        return the final component of a pathname
        '''
        return basename(self.path)

    def viewname(self) -> str:
        '''
        return the viewname of a scene
        '''
        return f'd="{self.released or ""}" p="{self.perfs_as_string()}" s="{self.paysite}" t="{self.title}"'

    def set_title(self, title: str = '') -> None:
        '''
        clean title, remove multiple spaces and assign it to the title
        '''
        t = ' '.join((title or '').split())
        t = sub(' part (\d+)', ' (Part \g<1>)', t, flags=IGNORECASE)
    # t = sub('\'[A-Z]', lambda x: x.group(0).lower(), m.group('title'))
        self.title = t # assign a fmt'd string

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
        mt = MimeTypes().guess_type(self.path)[0]
        if not mt:
            mt = 'video'
        return mt.replace(chr(47), chr(45)) # return mimetype

    def scan(self) -> None:
        '''
        read out video file's metadata using "ffprobe" (part of "ffmpeg")
        '''
        logger.debug(f'Scanning {self.viewname()}')
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
                logger.debug(
                    f'Suspicious Resolution {self.w}x{self.h}')
            if not cache(self.basename()):
                call(['ffmpeg',
                    '-ss', str(randrange(int(float(self.duration)))),
                    '-v',
                    'error',
                    '-i', self.path,
                    '-vframes', '1',
                    cache(self.basename(), True), '-y'])
                side = min(self.w, self.h)
                call(['convert',
                    cache(self.basename()),
                    '-gravity', 'Center',
                    '-crop', f'{side}x{side}+0+0',
                    #'-unsharp', '0.25x0.25+8+0.065',
                    '-resize', '49',
                    '-quality', '90', cache(self.basename())])
            self.ffprobed = True
        except (FileNotFoundError) as e:
            logger.warning(f'No such file or directory: {e.filename}')

        # be sure "ffprobe" is installed, run "apt install ffmpeg" otherwise

    def sanitize(self) -> str:
        '''
        return sanitized scene's name as a string
        '''
        name = basename(self.path)[:-4] # .lower()
        sep = '.' if name.count('.') > name.count(' ') else ' '
        for ss in list(['[pt]', '[', ']']):
            name = name.replace(ss, sep)
        droplist = ['720p','1080p','1920p','2160p','bj','int','mp4','mp4-gush','mp4-ktr','mp4-nbq','mp4-wrb','repack','xxx']
        return sep.join(
            x for x in name.split(sep) if x and x.lower() not in droplist)
