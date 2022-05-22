from enum import IntEnum


class RFCode(IntEnum):
    '''
    Possible opcodes returted by Remote Function Calls
    '''
    PERFORMER = 1
    TITLE = 2 # got a string as title
    SKIP_SCENE = 3 # skipped

    NOT_DEFINED = 0

# SxTools!MANAGER helps you to manage collections according to your wishes
