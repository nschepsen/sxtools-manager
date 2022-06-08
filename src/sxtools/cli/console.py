from os.path import abspath, exists
from typing import Tuple

from sxtools.core.manager import Manager, RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import REGEX, get_basic_logger

logger = get_basic_logger() # sXtools.log

'''
SxTools!MANAGER helps you to manage collections according to your wishes
'''

class Console:

    def __init__(self, m: Manager) -> None:
        '''
        Init the Non-GUI version of the app "SxTools!MANAGER
        '''
        self.manager = m # load manager
        self.manager.ui = self

    def fetch(self, path: str = None) -> None:
        '''
        '''
        if not path:
            path = self.manager.src
        sn = list([0]) # amount of newly added scenes
        for src in set([self.manager.out, path]):
            # check if the path exists
            if exists(src):
                self.manager.fetch(src)
                sn.append(len(self.manager.queue))
            else:
                logger.warning(f'The path "{src}" doesn\'t exist')
        logger.info(
            f'{len(self.manager.queue) - sn[0]} new scene(s) were added to the queue')

    def question(self, msg: str) -> bool:
        '''
        '''
        return input(f'> {msg} Type "yes" or "no": ').lower().strip() or 'yes' == 'yes'

    def decision(self, tail: str, s: Scene) -> Tuple[RFCode, str]:
        '''
        ask the user, he/she has to know the performer
        '''
        suggestion = '.'.join(tail.split('.')[:2])
        ret = input(f'> Does "{suggestion.replace(".", " ").title()}" perform in "{s}"? Type "skip" to abort ').lower().strip() or suggestion

        opcode = {
            'skip': RFCode.SKIP_SCENE,
            'title': RFCode.TITLE
            }.get(ret, RFCode.PERFORMER)

        return opcode, ret if ret!=suggestion else suggestion

    def exec(self) -> None:
        '''
        Execute the application, run through all stages
        '''
        self.fetch(self.manager.src) # ask user for some input
        while True:
            cmd = input('> ').strip() # use raw_input instead
            if cmd in [':v', 'version']:
                print(f'{self.manager.caption}')
            elif cmd == ':q':
                return
            elif cmd in [':cl', 'commandlist']:
                print([ # possible commands to the console
                    ':v - print the version',
                    ':q - quit',
                    ':s - save',
                    ':f[ path] - get scene(s)',
                    ':a - analyse',
                    ':cl'])
            elif cmd.startswith(':f'):
                self.fetch(abspath(' '.join(cmd.split()[1:])))
            elif cmd in [':a', 'analyse']:
                s: Scene # type hinting, just for "vs code"
                i = 0
                for s in self.manager.queue:
                    i += self.manager.analyse(s)
                    logger.debug(
                        f'\n-------------------------\n'
                        f'> Name: {s.name()}\n'
                        f'> Performers: {s.perfs_as_string()}\n'
                        f'> Released: {s.released} by {s.publisher} in {s.title or "None"}\n'
                        f'---------------------------')
                logger.info(f'Recognized: {i} of {len(self.manager.queue)} scene(s)')
            elif cmd == ':s':
                self.manager.save()
                for s in self.manager.queue:
                    self.manager.relocate(s)
            else:
                print(f'Unknown command: "{cmd}". Type "commandlist" to see all available commands')

# SxTools!MANAGER helps you to manage collections according to your wishes
