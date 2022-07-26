from datetime import date
from sxtools.utils import bview, fview, human_readable, sortmap, strtdate
from pytest import mark
from itertools import repeat

bviewTCases = zip([
    'Jynx Maze',    # case 1
    '   Jynx Maze', # case 2
    'Jynx Maze   ', # case 3
    ' Jynx  Maze ', # case 4
    'Jynx.Maze',    # case 5
    'jynx.maze'],   # case 6
    repeat('jynx.maze')) # expectation
@mark.parametrize('input, expected', bviewTCases)
def test_bview(input, expected):
    '''
    '''
    assert bview(input) == expected

fviewTCases = zip([
    'Jynx Maze',    # case 1
    '   Jynx Maze', # case 2
    'Jynx Maze   ', # case 3
    ' Jynx  Maze ', # case 4
    'Jynx.Maze',    # case 5
    'jynx.maze'],   # case 6
    repeat('Jynx Maze')) # expectation
@mark.parametrize('input, expected', fviewTCases)
def test_fview(input, expected):
    '''
    '''
    assert fview(input) == expected

strtdateTCases = zip([
    '2022-04-26',   # case 1
    '26-04-2022',   # case 2
    '2022.04.26',   # case 3
    '26.04.2022',   # case 4
    '22.04.26', '04.26.22'], # cases 5-6
    repeat(date(2022, 4, 26))) # expectation
@mark.parametrize('input, expected', strtdateTCases)
def test_strtdate(input, expected):
    '''
    '''
    assert strtdate(input) == expected

def test_sortmap():
    '''
    '''
    d = {'b': [2, 3, 1],
        'a' : {'c': ['b',
                'c',
                'a'],
            'a': 5782}}
    sortmap(d)
    assert d == {'a': {'a': 5782, 'c': ['a', 'b', 'c']}, 'b': [1, 2, 3]}

humanReadableTCases = [
    (0x00000000000180, '384.00 B'), # case 1
    (0x00000006d807, '438.01 KiB'), # case 2
    (0x00000024a46d2, '36.64 MiB'), # case 3
    (0x00000067b0c2ec, '1.62 GiB'), # case 4
    (0x0006726f619132, '6.45 TiB'), # case 5
    (0x0000000000000000, '0.00 B'), # case 6
    (0x01ce6bff2cd0f9d, '7.2 PiB')] # case 7
@mark.parametrize('input, expected', humanReadableTCases)
def test_human_readable(input, expected): assert human_readable(input) == expected