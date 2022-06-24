import logging
import sys
import argparse
from typing import Callable, NamedTuple
from functools import wraps

from rich.console import Console

from braillert.generator import generate_art
from braillert.colors import (
    DISCORD_COLORS,
    COLORAMA_COLORS,
    COLORAMA_RESETTER,
    RICH_COLORS,
    RICH_RESETTER
)
from braillert.logger import logger
from braillert.__init__ import __version__, __author__, __author_email__

class Palette(NamedTuple):
    """Palette type object"""
    printer: Callable = print
    palette: dict = None
    resetter: str = ''

FP_ARG_HELP_STRING: str = (
    """
    A required argument that represents the path where the convertible image is located
    e.g.
    --file-path=./my_folder/test.jpg
    """
)

MODE_ARG_HELP_STRING: str = (
    """
    A required argument that represents the mode in which the provided image should be converted
    e.g.
    --mode=rich or -m=discord
    """
)

WIDTH_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the width in which the provided image should be resized
    e.g.
    --width=100 or -w=50
    """
)

OUT_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the path in which the art should be saved
    e.g.
    --out=~/art.ansi or -o=./test.ansi
    """
)

THRESHOLD_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the threshold value that will be used
    during the art generation
    e.g.
    -t=150 or --threshold=100
    """
)

DISABLE_LOGGING_ARG_HELP_STRING: str = (
    """
    An optional argument that disables all text output in terminal, including logo,
    author and version
    e.g.
    -dl or --disable-logging
    """
)

LOGO_PATH = "./logo.ansi"
TEXT_LOGO: str
with open(LOGO_PATH, "r", encoding="utf-8") as logo_file:
    TEXT_LOGO = logo_file.read()

LOGO_DELIMITER_LENGTH = TEXT_LOGO.partition('\n')[0].count('⣿') # Not universal, must be replaced
LOGO_DELIMITER = '-' * LOGO_DELIMITER_LENGTH

palettes: dict = {
    "rich": Palette(printer=Console().print, palette=RICH_COLORS, resetter=RICH_RESETTER),
    "colorama": Palette(palette=COLORAMA_COLORS, resetter=COLORAMA_RESETTER),
    "discord": Palette(palette=DISCORD_COLORS),
    "gs": Palette()
}

sys.stdout.reconfigure(encoding="utf-8")

def _exception_handler(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error: #pylint: disable = broad-except
            logger.error("Error! Unexpected exception caught:")
            logger.info(str(error))

    return wrapper

@_exception_handler
def main() -> None:
    """Main function."""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-fp", "--file-path", dest="file_path",
                                        required=True, help=FP_ARG_HELP_STRING)
    argument_parser.add_argument("-m", "--mode", dest="mode", choices=palettes.keys(),
                                        default="rich", help=MODE_ARG_HELP_STRING)
    argument_parser.add_argument("-w", "--width", dest="width", type=int,
                                        default=100, help=MODE_ARG_HELP_STRING)
    argument_parser.add_argument("-o", "--out", dest="out", default=None, help=OUT_ARG_HELP_STRING)
    argument_parser.add_argument("-t", "--threshold", dest="threshold", default=None, type=int,
                                                                    help=THRESHOLD_ARG_HELP_STRING)
    argument_parser.add_argument("-dl", "--disable-logging", action="store_true",
                                                            help=DISABLE_LOGGING_ARG_HELP_STRING)

    arguments = argument_parser.parse_args()
    mode = palettes.get(arguments.mode)

    if arguments.disable_logging:
        logger.setLevel(logging.ERROR)
    else:
        Console().print(TEXT_LOGO + "\n\n")
        print(f"Author: {__author__} <{__author_email__}>  Version: {__version__}")
        print(LOGO_DELIMITER)

    logger.info("Generating...")
    art = generate_art(arguments.file_path, mode.palette, mode.resetter,
                            art_width=arguments.width, threshold=arguments.threshold)
    logger.success("Generated!")
    if arguments.out:
        with open(arguments.out, "w", encoding="utf-8") as out_file:
            out_file.write(art)
        logger.info("Saved to -> %s", arguments.out)
    else:
        mode.printer(art)
