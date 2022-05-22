from argparse import Namespace
from datetime import datetime
from hashlib import md5  # used for sitemap.json hashing
from os import listdir, makedirs, sep
from os.path import basename, dirname, exists, isdir, join, realpath
from re import search, split, sub
from rapidjson import dump, dumps, load
from shutil import move

from sxtools import __date__, __project__, __version__
from sxtools.core.rfcode import RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import REGEX, get_basic_logger

logger = get_basic_logger() # sXtools.log

'''
SxTools!MANAGER helps you to manage collections according to your wishes
'''

intview = lambda x: x.strip().lower().replace(' ', '.')

# accepted video formats

__VIDEO_EXT__ = (
    '.avi',
    '.f4v',
    '.flv',
    '.m4v',
    '.mkv',
    '.mov',
    '.mp4',
    '.wmv')
__MAGIC_NUM__ = 5

# FIXME: regex rules need a rework

__RE_SCN_ID__ = r'(?P<site>\w+)\.(?P<date>\d\d(\.\d\d){2})\.(?P<tail>[\w\.\-]+)'
__RE_LIB_ID__ = r'^\((?P<date>[\d\-]+)\)\s(?P<performers>[\w\.\s]+((,\s[\w\s]+)*(\s&\s[\s\w]+))?),\s(?P<site>[!&\-\w\'’\s().]+)(,\s(?P<title>.*))*'

class Manager:

    def __init__(self, args: Namespace) -> None:

        self.src = args.input
        self.out = args.output # used by GUI version
        self.top = args.top
        self.scan = not args.no_metadata
        self.dry = args.dryrun
        self.sorted = args.asc
        self.publishers = {}
        self.queue = list() # imported scenes
        self.app = dirname(dirname(realpath(__file__)))
        if args.dryrun:
            logger.info(f'Mode "DRY_RUN" activated')
        with open(join(self.app, 'sxtools.map.json'), 'r') as f:
            self.sitemap = load(f)
            self.build_sitemap() # self.sitemap
        self.hash = md5(dumps(self.sitemap, ensure_ascii=False).encode('utf8')).hexdigest()
        self.performers = {
            x: 0 for x in self.sitemap['performers']
            }
        logger.info(f'Loaded: {len(self.performers)} female performer(s)')

    def add_source(self, source: str) -> None:
        '''
        add a source directory
        '''
        if not isdir(source):
            logger.error(f'The directory "{source}" doesn\'t exist')
        else:
            self.src = source

        # TODO: self.emit('SourceDataChanged')

    def build_sitemap(self) -> None:
        '''
        build a sitemap containing sites, networks and performers
        '''
        unify = lambda s: s and ''.join([x for x in s if x.isalnum()]).lower()

        for network, sites in [
            *self.sitemap['networks'].items(), (None, self.sitemap['sites'])]:
            for site in sites:
                nid, sid = unify(network), unify(site)
            # choose your preferred publisher format:
                # network (site) vs. site
                publisher = f'{network} ({site})' if network else site
                if not network and self.publishers.get(sid, None):
                    logger.warning(f'"{site}" is already listed')
                self.publishers[sid] = publisher
                if network:
                    self.publishers[f'{nid}{sid}'] = publisher
        # match acronyms to the existing keys
        for acronym, v in self.sitemap.get('acronyms', {}).items():
            if acronym == v: # pqoc
                logger.warning(f'Remove the acronym "{acronym}"')
            publisher = self.publishers.get(unify(v))
            if publisher:
                self.publishers[acronym] = publisher
            else:
                logger.warning(f'The acronym "{acronym}" is undefined')
        logger.info(f'Loaded: {len(set(self.publishers.values()))} known site(s)')
        logger.warning(f'{len(self.sitemap["undefined"])} undefined key(s) detected')

    def fetch(self, target):
        '''
        recursively look for files in "self.src" and "self.out" directory
        '''
        for path in [join(target, f) for f in listdir(target)]:
            if isdir(path):
                self.fetch(path)
            elif path.lower().endswith(__VIDEO_EXT__):
                # known = [x.path for x in self.queue] # FIXME: performance
                if path not in [x.path for x in self.queue]:
                    self.queue.append(Scene(path, self.scan))
                else:
                    logger.debug(f'"{basename(path)}" is already added')
            else:
                logger.debug(f'The file "{basename(path)}" isn\'t a video')

    def analyse(self, s: Scene, ui) -> bool:
        '''
        analyse the scene and parse date, performers, publisher and title from it
        '''
        regexrules = [__RE_SCN_ID__, __RE_LIB_ID__]
    # TODO: by adding a new rule you have to verify the code for correctness
        m = next(
            filter(
                lambda c: c, map(lambda x: search(x, str(s)), regexrules)), None)
        if m is not None:
            date = m.group('date') # FIXME: better date parser
            if '.' in date: # %y.%m.%d format
                date = datetime.strptime(date, '%y.%m.%d').date()
            s.released = date # save date into the structure
            try:
                #s.title = m.group('title') or ''
                s.title = sub('\'[A-Z]', lambda m: m.group(0).lower(), m.group('title') or '')
                performers = [
                    intview(x) for x in split(',|&', m.group('performers'))]
            except IndexError as e:
                performers = list() # temp performer list
                tail = m.group('tail').lower()
                while True: # try to recognize all participating performers
                    performer = '' # reset
                    # look-ahead window range, up to 3 tokens
                    lookahead = range(min(tail.count('.') + 1, 3), 0, -1)
                    # look for already known performers
                    for key in ['.'.join(tail.split('.')[:x]) for x in lookahead]:
                        if key in self.performers and key.count('.') <= 0:
                             if ui.bool(f'Does {key} perform in {s}?'):
                                performer = key; break
                    if not performer: # there is no record in the dictionary
                        ret, performer = ui.rfc(tail, s)
                        if ret == RFCode.PERFORMER:
                            pass
                        elif ret == RFCode.TITLE:
                            break
                        elif ret == RFCode.SKIP_SCENE:
                            return False
                        else:
                            logger.warning(f'An unknown Code "{ret}" received')
                            return False
                    # append a performer to the performers list
                    performers.append(intview(performer)) # sinn?!
                    # update the "tail"-string
                    tail = tail[len(performer):].strip('.')
                    # check conditions for exiting the while loop
                    if not tail or 'and' not in tail:
                        break
                    if tail.startswith('and.'): tail = tail[4:] # erase string "and"
                s.title = tail.replace('.', '').title()
            # update the stats, participating performers
            for x in performers:
                self.performers[x] = self.performers.get(x, 0) + 1
            s.performers = sorted(
                [x.replace('.', ' ').title() for x in performers]) # save performers
            sid = ''.join([x for x in m.group('site') if x.isalnum()]).lower()
            publisher = self.publishers.get(sid, sid)
            if publisher == sid and sid not in self.sitemap['undefined']:
                self.sitemap['undefined'].append(sid)
                logger.info(f'A new site "{sid}" added')
            s.publisher = publisher # save scene publisher
            return True
        logger.log(REGEX, f'The scene doesn\'t match to the regex: "{s}"'); return False

    def relocate(self, s: Scene) -> None:
        '''
        try to move a scene into the library directory
        '''
        if self.dry:
            logger.debug('Won\'t relocate the scene, DRY_MODE is on!')
            return
        if not s.released or not s.performers or not s.publisher:
            # # there's no metadata, so it couldn't be renamed
            # if DONTMOVEFLAG:
            #     logger.debug(
            #         f'Won\'t move "{basename(s.path)}"')
            target = f'{sep}'.join(
                [sep.join(self.out.split(sep)[:-1]), 'unsorted', basename(s.path)])
        else:
            n, famous = max([(self.performers[intview(i)], i) for i in s.performers])
            # try to move the scene into the target library
            suffix = join(famous[0], famous)
            if n < __MAGIC_NUM__:
                suffix = 'Miscellany'
            # build a new video scene name according to the library format
            filename = '({}) {}, {}{}.{}'.format(
                s.released,
                s.perfs_as_string(),
                s.publisher,
                f', {s.title}' if s.title else '', s.ext)
            target = join(join(self.out, suffix), filename)
        # check if the scene exists
        if s.path != target:
            logger.debug(f'The new scene location is "{target}"')
            if not exists(target):
                makedirs(
                    dirname(target), exist_ok=True)
                move(s.path, target); s.path = target
            else:
                logger.warning(f'Oops! A copy of "{basename(target)}" already exists!')

        # TODO: the current directory has to be deleted if it doesn't contain any video files

    def save(self) -> None:
        '''
        save sitemap to the file if any changes occurred
        '''
        # sort performers in ascending order
        self.sitemap['performers'] = sorted(self.performers.keys())
        # count performers participated in fetched scenes
        performers = sum(
            x > 0 for k, x in self.performers.items())
        # examine sitenmap for changes
        if self.hash != md5(dumps(self.sitemap, ensure_ascii=False).encode('utf8')).hexdigest():
            if not self.dry:
                with open(join(self.app, 'sxtools.map.json'), 'w') as f:
                    dump(self.sitemap, f)
            logger.info('Saving sitemap in DRY_MODE takes no changes')
        logger.info(f'{performers} actors perform in {len(self.queue)} scenes produced by n sites')

# SxTools!MANAGER helps you to manage collections according to your wishes
