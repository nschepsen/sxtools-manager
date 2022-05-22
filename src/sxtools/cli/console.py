from os.path import exists
from posixpath import basename
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

    def exec(self) -> None:
        '''
        Execute the application, run through all stages
        '''
        for src in set([self.manager.out, self.manager.src]):
            # check if the path exists
            if exists(src):
                self.manager.fetch(src)
            else:
                logger.warning(f'The path "{src}" doesn\'t exist')


        n = len(self.manager.queue) # size of the queue
        logger.info(f'{n} scene(s) were discovered in storages')
        i = 0
        for s in self.manager.queue:
            ret = self.manager.analyse(s, self)
            i += ret
            # if ret:
            #     logger.debug(
            #         f'\n------------------------\n'
            #         f'File: {basename(s.path)}\n'
            #         f'Date: {s.released}\n'
            #         f'Performers: {s.performers}\n'
            #         f'Publisher: {s.publisher}\n'
            #         f'Title: "{s.title}"\n'
            #         f'------------------------\n'
            #         )

        logger.debug(f'Erfolgreich erkannt: {i} of {n}'); self.manager.save()

        for s in self.manager.queue:
            self.manager.relocate(s)

    def bool(self, msg: str) -> bool:
        '''
        '''
        return input(f'> {msg} Type "yes" or "no":').lower().strip() or 'yes' == 'yes'

    def rfc(self, tail: str, s: Scene) -> Tuple[RFCode, str]:
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

# SxTools!MANAGER helps you to manage collections according to your wishes
