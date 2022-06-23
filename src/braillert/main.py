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

CONTRAST_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the contrast value in which the art should be modified
    e.g.
    -c=1.5 or --contrast=1.3
    """
)

CONTRAST_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the threshold value that will be used
    during the art generation
    e.g.
    -t=150 or --threshold=100
    """
)

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
            logger.error("Error! Unexpected exception caught: %s", *error.args)

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
    argument_parser.add_argument("-c", "--contrast", dest="contrast", default=None, type=float)
    argument_parser.add_argument("-t", "--threshold", dest="threshold", default=None, type=int)

    arguments = argument_parser.parse_args()
    mode = palettes.get(arguments.mode)

    logger.info("Generating...")
    art = generate_art(arguments.file_path, mode.palette, mode.resetter,
                            art_width=arguments.width, contrast=arguments.contrast, threshold=arguments.threshold)
    logger.success("Generated!")
    if arguments.out:
        with open(arguments.out, "w", encoding="utf-8") as file:
            file.write(art)
        logger.info("Saved to -> %s", arguments.out)
    else:
        mode.printer(art)
