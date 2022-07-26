from itertools import zip_longest as zipl
from os.path import abspath, exists
from typing import Tuple

from sxtools.core.manager import Manager, RFCode
from sxtools.core.videoscene import Scene
from sxtools.logging import get_basic_logger
from sxtools.utils import fview

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
                print([ # list of possible commands
                    ':v - print the version',
                    ':q - quit',
                    ':s - save',
                    ':f[ path] - get scene(s)',
                    ':a - analyse',
                    ':cl'])
            elif cmd.startswith(':f'):
                self.fetch(abspath(' '.join(cmd.split()[1:])))
            elif cmd.startswith('top'):
                top = int(' '.join(cmd.split()[1:]) or self.manager.top)
                perfs = sorted(self.manager.performers.items(), key=lambda x: x[1], reverse=True)[:top]
                paysites = {}
                x: Scene
                for x in self.manager.queue:
                    if x.paysite:
                        paysites[x.paysite] = paysites.get(x.paysite, 0) + 1
                paysites = sorted(paysites.items(), key=lambda x: x[1], reverse=True)[:top]
                if not paysites: # list is empty
                    logger.warning(
                        'Perform an analysis (:a) or The queue contains unregexable scene(s) only!')
                    break
                data = [('Top', 'Performer', 'Count', 'Paysite', 'Count'), *[(x, y[0][0], y[0][1], y[1][0], y[1][1]) for x, y in zip(range(1, len(perfs) + 1), zipl(perfs, paysites))]]
                for id, performer, pc, paysite, sc in data:
                    print(f'{str(id).zfill(3):^{5}} {fview(performer):^{20}} {pc:^{5}} {paysite:^{40}} {sc:^{5}}')
            elif cmd in [':a', 'analyse']:
                s: Scene # type hinting, just for "vs code"
                i = 0
                for s in self.manager.queue:
                    i += self.manager.analyse(s)
                    logger.debug(
                        f'\n-------------------------\n'
                        f'> Name: {s.viewname()}\n'
                        f'> Performers: {s.perfs_as_string()}\n'
                        f'> Released: {s.released} by "{s.paysite}" in "{s.title}"\n'
                        f'---------------------------')
                logger.info(f'Recognized: {i} of {len(self.manager.queue)} scene(s)')
            elif cmd == ':s':
                self.manager.save()
                for s in self.manager.queue:
                    self.manager.relocate(s)
            else:
                print(f'Unhandled command: "{cmd}". Type "commandlist" to see all available commands')

# SxTools!MANAGER helps you to manage collections according to your wishes
