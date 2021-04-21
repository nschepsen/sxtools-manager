#!/usr/bin/python3

from os import listdir, makedirs, path
from re import IGNORECASE, match, search
from shutil import move
from sys import argv, exit
from time import process_time as measure
from hashlib import md5

from rapidjson import load, dump, dumps

import logging  # used for debugging (SXTools.log)

h1 = lambda title: '--- [' + title.title() + '] ' + (30 - len(title)) * '-'

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
__RE_VSNAME__ = r'^\((?P<date>[\d\-]+)\)\s(?P<performers>[\w\.\s]+((,\s[\w\s]+)*(\s&\s[\s\w]+))?),\s(?P<site>[!&\-\w\'’\s().]+)(,\s(?P<title>.*))*\.(?P<ext>' + '|'.join([x[1:] for x in __VIDEO_EXT__]) + ')'

class Organizer:

    performers, sites, library = {}, {}, {}; warnings = 0; db = []

    def __init__(self, args: list = []):

        self.__PROJECT__ = 'Organizer!SXTools'
        self.__VERSION__ = '1.0.20210421'
        # create & configure the logger
        logging.basicConfig(
            filename='SXTools.log',
            filemode='a',
            datefmt='%d %b %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
        # log the welcome message
        logging.info(f'{self.__PROJECT__} v{self.__VERSION__}')

        if any(opt in argv for opt in ['-h', '--help']):
            self.help(); return
        self.app = path.dirname(path.realpath(__file__))

        self.src = path.join(self.app, 'source') # --src=PATH
        self.top = 30 # or pass --top=XXX, as an argument
        self.dry = False # --dry-run
        self.asc = False # --asc
        self.out = path.join(self.app, 'target') # --out=PATH

        for arg in args: # handle passed arguments

            logging.debug(f'passed through args {arg}')

            if arg == '--dry-run':
                self.dry = True
            elif '--asc' in arg:
                self.asc = True
            elif '--src' in arg:
                self.src = arg.split('=')[1]
            elif '--out' in arg:
                self.out = arg.split('=')[1]
            elif '--top' in arg:
                self.top = int(arg.split('=')[1])
            else:
                print(f'[WARN] Unknown Argument: "{arg}".')

        self.out = self.src if self.out == path.join(self.app, 'target') else self.out

        if self.dry: print('[INFO] running in DRY_RUN mode')

        with open(path.join(self.app, 'sxtools.map.json'), 'r') as f:
            self.sitemap = load(f)
        self.hash = md5(dumps(self.sitemap, ensure_ascii=False).encode('utf8')).hexdigest()

    def help(self):

        print (
            f'\n'
            f'USAGE: python3 {__file__.split(chr(47))[-1]} [option], where option\n'
            f'\n'
            f' --asc\n  sort performers and sites in ascending order\n'
            f' --dry-run\n  analyze data only (don\'t operate on it)\n'
            f' -h, --help\n  print this help message and exit (also --help)\n'
            f' --out=PATH\n  set the output folder\n'
            f' --src=PATH\n  set the source folder\n'
            f' --top=XXX\n  limit the top charts by XXX performers and sites\n'
            f' -v, --version\n  show the current version\n'
            f'\n'
            f'{self.__PROJECT__} v{self.__VERSION__} (check for updates @ GitHub)\n'
        )

    def analyse(self, src: str):

        ''' This Method Analyses Scenes Counting Performers & Sites And Corrects The Scene Identifiers '''

        for scene in [path.join(src, f) for f in listdir(src)]:
            plain = path.basename(scene)
            # scene is a directory
            if path.isdir(scene):
                self.analyse(scene)
            # scene is a file
            elif scene.lower().endswith(__VIDEO_EXT__):
                m = search(__RE_VSNAME__, plain, IGNORECASE)
                if m is not None:
                    date = m.group('date')
                    ext = m.group('ext').lower()
                    performers = sorted([
                        i.strip() for i in m.group('performers').replace('&', ',').split(',')])
                    sid = ''.join([x for x in m.group('site') if x.isalnum()]).lower()
                    site = self.library.get(sid, 'undefined')
                    if site == 'undefined':
                        self.sitemap['undefined'].append(sid)
                        logging.info(
                            f'ignore scene "{plain}" due to unknown sid')
                        continue
                    title = m.group('title') # title could be empty
                    for actor in performers:
                        self.performers[actor] = self.performers.get(actor, 0) + 1
                    self.sites[site] = self.sites.get(site, 0) + 1
                    actors = ', '.join(performers[:-2] + [' & '.join(performers[-2:])])
                    # correct the scene identifier
                    new = f'({date}) {actors}, {site}{", " + title if title else ""}.{ext}'
                    if new != plain and not self.dry:
                        logging.info(f'rename {plain} to {new}')
                        move(scene, path.join(src, new))
                    self.db.append({ 'path': src, 'id': new, 'performers': performers })
                else:
                    self.warnings += 1
                    logging.warning(f'ignore "{plain}" due to unmatch to the regex')
            else:
                logging.debug(f'ignore "{plain}", it seems not to be a scene, continue to the next scene')

    def run(self):

        ''' STEP 1: B U I L D  T H E  L I B R A R Y '''

        escape = lambda s: s and ''.join([x for x in s if x.isalnum()]).lower()

        t0 = measure()

        for network, sites in [*self.sitemap['networks'].items(), (None, self.sitemap['sites'])]:
            for site in sites:
                nid, sid = escape(network), escape(site)
            # choose your prefered publisher format:
                # Network (Site) vs. Site
                value = f'{network} ({site})' if network else site
                self.library[sid] = value
                if network: self.library[f'{nid}{sid}'] = value
        # match acronyms to the existing keys
        for acronym, v in self.sitemap.get('acronyms', {}).items():
            self.library[acronym] = self.library.get(escape(v), 'undefined')
            if self.library[acronym] == 'undefined':
                logging.warning(f'The acronym "{acronym}" is undefined')
        # calculate the sitemap build up execution time
        print(f'The sitemap library was built in {1e3 * (measure() - t0):.5f} milliseconds')

        ''' STEP 2: T R A V E R S E  F O L D E R S '''

        for storage in set([self.out, self.src]):
            # check if the given path exists
            if path.exists(storage):
                self.analyse(storage)
            else:
                print('[WARN] The specified path does not exist')
        self.sitemap['undefined'] = sorted(set(self.sitemap['undefined']))

        ''' STEP 3: R E N A M E  S C E N E S  A C C O R D I N G  TO  S C H E M A '''

        for scene in self.db:
            if self.out in scene.get('path') and 'Miscellany' not in scene.get('path'):
                continue
            famous = max([(self.performers[i], i) for i in scene.get('performers')])
            if not self.dry:
                target = path.join(famous[1][0], famous[1])
                if famous[0] < __MAGIC_NUM__:
                    target = 'Miscellany'
                target = path.join(self.out, target)
                if scene['path'] != target:
                    makedirs(target, exist_ok=True)
                    move(path.join(scene['path'], scene['id']), path.join(target, scene['id']))

        ''' STEP 4: U P D A T E  T H E  S I T E M A P '''

        if self.hash != md5(dumps(self.sitemap, ensure_ascii=False).encode('utf8')).hexdigest():
            with open(path.join(self.app, 'sxtools.map.json'), 'w') as f:
                dump(self.sitemap, f)
        print(f'[INFO] {len(self.performers)} actors perform in {len(self.db)} movies produced by {len(self.sites)} studios')

        ''' STEP 5: V I S U A L I Z E  P A R S E D  D A T A '''

        if not len(self.db): return # RETURN if self.db empty is
        self.performers = dict(sorted(
            self.performers.items(), key=lambda x: x[0] if self.asc else x[1], reverse=not self.asc))
        self.sites = dict(sorted(self.sites.items(), reverse=not self.asc, key=lambda x: x[0] if self.asc else x[1]))
        sliced = dict([*list(self.performers.items())[:self.top],
        *list(map(
            lambda x: (x[0] if chr(40) not in x[0] else x[0][x[0].index(chr(40)) + 1:-1], x[1]),
            self.sites.items()))[:self.top]])
        self.top = min(self.top, len(self.performers))
        gap = max(28, max(map(lambda x: len(f'{x[0]}{x[1]}'), sliced.items())) + 1)
        print(h1(f'Top {self.top} Performers'))
        for k, v in list(sliced.items())[:self.top]:
            print(f'・{k} {(gap - len(k) - len(str(v))) * "."} {v}')
        print(h1(f'Top {self.top} Sites'))
        for k, v in list(sliced.items())[self.top:]:
            print(f'・{k} {(gap - len(k) - len(str(v))) * "."} {v}')
        print(h1('Duplicates'))
        seen = set()
        for i in [x for x in list(map(str.lower, [*self.performers, *self.sites])) if x in seen or seen.add(x)]:
            print(f'・{i} {(gap - len(i)) * "."} warning')
        if len(seen) == len([*self.performers, *self.sites]):
            print('・No duplicate values found')
        # print(h1('Suspicious'))
        # for i in sorted([x for x in self.performers.keys() if len(x.split()) != 2], reverse=True, key=lambda item: len(item.split())):
        #     print(f'・{i} {(gap - len(i) - 1) * "."} {len(i.split())}')
        print('-------------------------------------')

def main(): # ''' END ''' #

    Organizer(argv[1:]).run()

if __name__ == "__main__": main()  # Organizer!SXTools v1.0.20210421
