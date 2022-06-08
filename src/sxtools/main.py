from argparse import ArgumentParser
from os import getcwd, path

from sxtools import __project__, __version__
from sxtools.cli.console import Console
from sxtools.core.manager import Manager
from sxtools.logging import get_basic_logger
logger = get_basic_logger() # sXtools.log
from sxtools.utils import apt_path_exists, check_updates  # path pre-check

def main():

    '''
    Here is the ENTRYPOINT for pip, cli and GUI versions
    '''

    parser = ArgumentParser(description=f'{__project__} helps you to manage collections according to your wishes')
    # add cli arguments
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-v', '--verbose',
        action='count',
        help='verbose mode: info & debug',
        default=0) # logging.level = WARNING
    verbosity.add_argument(
        '-q', '--quiet',
        action='count',
        help='less output: warnings & criticals',
        default=0) # logging.level = WARNING
    parser.add_argument(
        '--gui', '--qt',
        action='store_true',
        default=False,
        help='launch the app in windowed mode')
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        default=False,
        dest='dryrun',
        help='run the app without taking any changes to files and the "map" library')
    parser.add_argument(
        '--input',
        help=f'set a path to sources',
        metavar='PATH',
        type=apt_path_exists,
        default=getcwd()) # sources
    parser.add_argument(
        '--output',
        help='set a path to an output directory (default: "$input")',
        metavar='PATH',
        type=path.abspath,
        default=None) # use $input as default
    parser.add_argument(
        '-t', '--top',
        type=int,
        help='limit the "in-app table size" to n rows',
        default=30) # limit the output to n rows
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        dest='wo_analyse',
        help='don\'t use ffprobe to get metadata',
        default=False)
    parser.add_argument(
        '--asc',
        action='store_true',
        help='sort the output in ascending order')
    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'{__project__} v{__version__}')
    args = parser.parse_args()
    if not args.output:
        args.output = args.input # path.join(args.input, 'library')
    if args.verbose or args.quiet:
        # set logger level
        logger.setLevel(10 * (3 + min(args.quiet, 3) - min(args.verbose, 2)))
    manager = Manager(args)
    if args.gui:
        try:
            from PySide6.QtWidgets import QApplication
            from sxtools.ui.mainwindow import MainWindow
            app = QApplication([])
            window = MainWindow(manager)
            window.show(); exit(app.exec())
        except ModuleNotFoundError as error:
            logger.error(f'{error.__class__.__name__}: {error}')
    else:
        Console(manager).exec() # Run NON-GUI version

# SxTools!MANAGER helps you to manage collections according to your wishes
