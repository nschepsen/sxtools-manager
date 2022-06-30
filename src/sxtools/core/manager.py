from argparse import Namespace
from hashlib import md5, shake_128  # used for sitemap.json hashing to detect changes
from os import listdir, makedirs, sep
from os.path import basename, dirname, exists, getsize, isdir, join, realpath
from re import search, split  #, sub
from shutil import move
try:
    from rapidjson import dump, dumps, load
except ImportError:
    from json import dump, dumps, load
from sxtools import __date__, __project__, __version__
from sxtools.core.rfcode import RFCode  # FIXME: any WAs maybe?!
from sxtools.core.videoscene import Scene
from sxtools.logging import REGEX, get_basic_logger
logger = get_basic_logger()  # sXtools.log
from sxtools.utils import bview, cache, fview, human_readable, sortmap, strtdate  # back-&frontend repr

'''
SxTools!MANAGER helps you to manage collections according to your wishes
'''

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
        self.out = args.output
        self.top = args.top # used by CLI only
        self.is_analyse_req = args.scan
        self.dry = args.dryrun
        self.asc = args.asc
        self.caption = f'{__project__} v{__version__}'
        self.publishers = {}
        self.scenes, self.queue = list(), list()
        self.app = dirname(dirname(realpath(__file__)))
        logger.info(f'{self.caption}')
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
                p = f'{network} ({site})' if network and nid != sid else site
                if not network and self.publishers.get(sid):
                    logger.warning(f'"{site}" is already listed')
                self.publishers[sid] = p
                if network:
                    self.publishers[f'{nid}{sid}'] = p
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

    def save(self) -> None:
        '''
        dump sitemap to a file sorting by keys and then by values in ascending order
        '''
        self.sitemap['performers'] = [*self.performers]
        sortmap(self.sitemap)
        # count performers participated in fetched scenes
        performers = sum(
            v > 0 for v in self.performers.values())
        # examine sitenmap for changes
        if self.hash != md5(dumps(self.sitemap, ensure_ascii=False, sort_keys=True).encode('utf8')).hexdigest():
            if not self.dry:
                with open(join(self.app, 'sxtools.map.json'), 'w') as f:
                    dump(self.sitemap, f)
                logger.info('Sitemap changes were successfully saved')
            else:
                logger.info('Saving sitemap in DRY_MODE takes no changes')
        logger.info(f'Statistics: {performers} actors perform in {len(self.queue)} scenes')

    def fetch(self, directory: str) -> None:
        '''
        perform a recursive search to get v-files from source directories
        '''
        for path in [join(directory, f) for f in listdir(directory)]:
            if isdir(path):
                self.fetch(path)
            elif path.lower().endswith(__VIDEO_EXT__):
                # FIXME: problems?! implement a WA to avoid duplicates
                if path not in [x.path for x in self.queue]:
                    s = Scene(path)
                    if self.is_analyse_req:
                        s.scan()
                    self.queue.append(s)
            else:
                logger.debug(f'The file "{basename(path)}" isn\'t a video')

    def analyse(self, s: Scene) -> bool:
        '''
        tokenize the scene name and parse date, performers, publisher and title, if possible
        '''
        regexrules = [__RE_SCN_ID__, __RE_LIB_ID__] # by adding new rules, verify the code
        m = next(filter(bool, map(search, regexrules, [str(s)] * len(regexrules))), None)
        if m is None:
            logger.log(REGEX, f'The scene doesn\'t match to the regex: "{s}"')
            return False
        s.released = strtdate(m.group('date')) # save date
        sid = ''.join(x for x in m.group('site') if x.isalnum()).lower()
        publisher = self.publishers.get(sid)
        if not (publisher or sid in self.sitemap['undefined']):
            self.sitemap['undefined'].append(sid)
            logger.info(f'A new publisher site "{sid}" added')
        s.paysite = publisher or sid # save scene publisher into the structure
        try:
            s.set_title(m.group('title')) # See the setTitle() implementation!
            # opt: sub('\'[A-Z]', lambda x: x.group(0).lower(), m.group('title'))
            performers = [bview(x) for x in split(',|&', m.group('performers'))]
        except IndexError as e:
            performers = list() # temp bviewed performer list
            tail = m.group('tail').lower()
            while True: # FIXME: implement a better logic for "performer search"
                performer = '' # init&reset local variable
                # look-ahead window range, up to 3 tokens
                lookahead = range(min(tail.count('.') + 1, 3), 0, -1)
                # look for already known performers
                for key in ['.'.join(tail.split('.')[:x]) for x in lookahead]:
                    if key in self.performers:
                        question = f'Does "{key.title()}" perform in "{tail}"?'
                        if not (key.count('.') or self.ui.question(question)):
                            continue
                        performer = key; break
                if not performer: # no records found, perform a manual search
                    ret, performer = self.ui.decision(tail, s)
                    if ret == RFCode.PERFORMER:
                        pass # everything is OK, go to the next instruction
                    elif ret == RFCode.TITLE:
                        break # leave the loop, the tail contains "title" only
                    elif ret == RFCode.SKIP_SCENE:
                        return False # attention! something went wrong
                    else: logger.warning(f'An unknown Code "{ret}" received'); return False
                # append a performer to the performers list
                performers.append(bview(performer)) # sinn?!
                # update the "tail"-string
                tail = tail[len(performer):].strip('.')
                # check conditions for exiting the while loop
                if not tail or 'and.' not in tail:
                    break
                if tail.startswith('and.'): tail = tail[4:] # erase string "and"
            s.set_title(fview(tail)) # format the tail using predefined "fview"-fmt
        # collection main statistics, update the database, count performers & publisher
        for x in performers:
            self.performers[x] = self.performers.get(x, 0) + 1
        s.performers = sorted(fview(x) for x in performers); return True # save performers

    def relocate(self, s: Scene) -> None:
        '''
        move a scene file into the library directory, handle duplicates
        '''
        if self.dry:
            logger.debug('Won\'t relocate the scene, DRY_MODE is on!')
            return
        if not s.released or not s.performers or not s.paysite: # use not s.in_valid() instead
            # # there's no metadata, so it couldn't be renamed
            # if DONTMOVEFLAG:
            #     logger.debug(
            #         f'Won\'t move "{basename(s.path)}"')
            target = f'{sep}'.join(
                [sep.join(self.out.split(sep)[:-1]), 'unsorted', s.basename()])
        else:
            n, famous = max([(self.performers[bview(i)], i) for i in s.performers])
            # try to move the scene into the target library
            suffix = join(famous[0], famous)
            if n < __MAGIC_NUM__:
                suffix = 'Miscellany'
            # build a new video scene name according to the library format
            filename = '({}) {}, {}{}.{}'.format(
                s.released,
                s.perfs_as_string(),
                s.paysite,
                f', {s.title}' if s.title else '', s.ext)
            target = join(join(self.out, suffix), filename)
        # check if the scene exists
        if s.path != target:
            logger.debug(f'The new scene location is goin\' to be "{target}"')
            isMoveable = True
            if exists(target):
                logger.warning(
                    f'Oops! A copy already exists: "{basename(target)}"')
                s1, s2 = human_readable(getsize(target)), human_readable(s.size)
                isMoveable = self.ui.question(
                    f'Do you want to replace it "{s1}" with yours copy "{s2}"? ')
            if isMoveable:
                makedirs(
                    dirname(target), exist_ok=True)
                thumbnail = cache(s.basename())
                if s.basename() != basename(target) and thumbnail:
                    move(thumbnail, cache(basename(target), True))
                move(s.path, target); s.path = target # Good Luck! my friend

        # TODO: the current directory has to be deleted if it doesn't contain any video files

# SxTools!MANAGER helps you to manage collections according to your wishes
