from argparse import Namespace
from hashlib import md5  # used for sitemap.json hashing to detect changes
from os import listdir, makedirs, sep
from os.path import basename, dirname, exists, getsize, isdir, join, realpath
from re import search, split  # , sub
from shutil import move
from rapidjson import dump, dumps, load
from sxtools import __date__, __project__, __version__
from sxtools.core.rfcode import RFCode  # FIXME: any WAs maybe?!
from sxtools.core.videoscene import Scene
from sxtools.logging import PARSE, REGEX, get_basic_logger
from sxtools.utils import bview, cache, fview, human_readable, sortmap, strtdate, unify

scheme = list([

    r'^d="(?P<date>.*)" p="(?P<performers>.*)" s="(?P<site>.*)" t="(?P<title>.*)"', # SEMIPARSED
    r'(?P<site>\w+)\.(?P<date>\d\d(\.\d\d){2})\.(?P<tail>[\w\.\-]+)', # SCENE
    r'^\((?P<date>[\d\-]+)\)\s(?P<performers>[\w\.\s]+((,\s[\w\s]+)*(\s&\s[\s\w]+))?),\s(?P<site>[!&\-\w\'’\s().]+)(,\s(?P<title>.*))*']) # LIBRARY

logger = get_basic_logger()

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


class Manager:

    def __init__(self, args: Namespace) -> None:

        self.src = args.input
        self.out = args.output
        self.top = args.top # limits the output to default: 30
        self.is_analyse_req = args.scan
        self.dry = args.dryrun
        self.asc = args.asc
        self.caption = f'{__project__} v{__version__}'
        self.queue = list() # stores scenes
        self.sitemap = {}
        self.app = dirname(dirname(realpath(__file__)))
        logger.info(f'{self.caption}')
        if args.dryrun:
            logger.info(f'Mode "DRY_RUN" activated')
        with open(join(self.app, 'sxtools.map.json'), 'r') as f:
            self.cfg = load(f)
            self.build_sitemap() # populate sitemap w known sites
        self.hash = self.footprint()
        self.paysites = {} # empty at start TODO: implement Stats
        self.performers = {
            x: 0 for x in self.cfg['performers']
            }
        logger.info(
            f'The DB contains {len(self.performers)} performer(s)')

    def footprint(self) -> str:
        '''
        calculate a hash value for the current config's state
        '''
        return md5(dumps(self.cfg, ensure_ascii=False).encode('utf8')).hexdigest()

    def save(self) -> None:
        '''
        store "config" into a file sorting by keys and then by values
        '''
        self.cfg['performers'] = [*self.performers]
        sortmap(self.cfg)
        # count performers in current scenes
        performers = sum(
            v > 0 for v in self.performers.values())
        # check a local copy of config for changes
        if self.hash != self.footprint():
            if not self.dry:
                with open(join(self.app, 'sxtools.map.json'), 'w') as f:
                    dump(self.cfg, f)
                logger.info('Configs saved successfully')
        logger.info(
            f'Live Stats: {performers} actors perform in {len(self.queue)} scenes')

    def reset(self) -> None:
        '''
        nullify the manager's live statistics
        '''
        for k, v in self.performers.items():
            self.performers[k] = 0
        if self.queue: self.queue.clear() # empty the queue

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
            *self.cfg['networks'].items(), (None, self.cfg['sites'])]:
            for site in sites:
                nid, sid = unify(network), unify(site)
            # choose your preferred publisher format:
                # network (site) vs. site
                p = f'{network} ({site})' if network and nid != sid else site
                if not network and self.sitemap.get(sid):
                    logger.warning(f'"{site}" is already listed')
                self.sitemap[sid] = p
                if network:
                    self.sitemap[f'{nid}{sid}'] = p
        # match acronyms to the existing keys
        for acronym, v in self.cfg.get('acronyms', {}).items():
            if acronym == v: # pqoc
                logger.warning(f'Remove the acronym "{acronym}"')
            publisher = self.sitemap.get(unify(v))
            if publisher:
                self.sitemap[acronym] = publisher
            else:
                logger.warning(f'The acronym "{acronym}" is undefined')
        logger.info(f'Loaded: {len(set(self.sitemap.values()))} known site(s)')
        logger.warning(f'{len(self.cfg["undefined"])} undefined key(s) detected')

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
        parse date, performers, paysite and title & track statistics
        '''
        m = next(filter(bool, map(search, scheme, [str(s)] * len(scheme))), None)
        if m is None:
            s.set_title(str(s))
            logger.log(
                REGEX,
                f'The scene doesn\'t match the regex: "{s}"')
            return False
        s.released = strtdate(m.group('date')) # save parsed date
        sid = ''.join(x for x in m.group('site') if x.isalnum()).lower() # non-unique
        paysite = self.sitemap.get(sid)
        if not (paysite or sid in self.cfg['undefined']):
            self.cfg['undefined'].append(sid)
            logger.info(f'A new paysite "{sid}" added to the queue')
        else:
            pid = unify(paysite) # generate unique identifier
            self.paysites[pid] = self.paysites.get(pid, 0) + 1
        s.paysite = paysite or sid # save paysite into the structure
        try:
            s.set_title(m.group('title')) # function modifies the string
            performers = [bview(x) for x in split(',|&', m.group('performers')) if x]
        except IndexError as e:
            performers, tail = list(), m.group('tail').lower() # reset
            while True: # FIXME: implement a better logic aka perf parser
                performer = '' # reset local variables
                # look-ahead window range, up to 3 tokens
                lookahead = range(min(tail.count('.') + 1, 3), 0, -1)
                # does the perf DB contain one of these tokens?
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
        s.performers = sorted(fview(x) for x in performers)
        logger.log(PARSE, s.viewname())
        return True # The analyse is complete & The scene should be at least semiparsed now

    def relocate(self, s: Scene) -> None:
        '''
        move a scene "s", eliminate duplicates & remove empty folders
        '''
        if self.dry:
            logger.debug('Move-Op isn\'t possible due to DRY_MODE')
            return
        if not s.released or not s.performers or not s.paysite:
            # if DONTMOVEFLAG:
            #     return
            suffix = 'Unsorted' # folder for unsorted scenes
            fn = 'd="{}" p="{}" s="{}" t="{}".{}'.format(
                s.released or '', s.perfs_as_string(), s.paysite, s.title, s.ext)
        else:
            n, famous = max(
                (self.performers.get(bview(i), 1), i) for i in s.performers)
            # define a scene's and lib subfolder's name
            suffix = join(famous[0], famous)
            fn = '({}) {}, {}{}.{}'.format(
                s.released or '',
                s.perfs_as_string(), s.paysite, f', {s.title}' if s.title else '', s.ext)
            if n < __MAGIC_NUM__:
                suffix = 'Miscellany'
        target = f'{sep}'.join([self.out, suffix, fn]) # full fn w path
        # check if there is a file w the same path;  no need to operate on it
        if s.path != target:
            isMoveable = True # each scene is moveable by default
            logger.debug(f'Trying to save "{fn}" in "{suffix}"')
            if exists(target):
                logger.warning(
                    f'Oops! A copy of "{fn}" already exists')
                old, new = human_readable(getsize(target)), human_readable(s.size)
                isMoveable = self.ui.question(
                    f'Do you want to replace "{old}" with "{new}"?')
            if isMoveable:
                makedirs(dirname(target), exist_ok = True) # be sure, the folder exists
                thumbnail = cache(s.basename())
                if s.basename() != basename(target) and thumbnail:
                    move(thumbnail, cache(basename(target), True))
                move(s.path, target); s.path = target # Good Luck! my friend

        # TODO: the current directory has to be deleted if it doesn't contain any video files

# SxTools!MANAGER helps you to manage collections according to your wishes
