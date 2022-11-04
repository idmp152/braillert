import argparse
import logging
import os
import sys
from functools import wraps
from time import sleep
from typing import Callable

from PIL import Image

from braillert.__init__ import __author__, __author_email__, __version__
from braillert.colors import AvailableColors
from braillert.exceptions import (GifUnsupportedResizeError,
                                  GifUnsupportedSaveError)
from braillert.generator import Generator
from braillert.logger import logger


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

GIF_ARG_HELP_STRING: str = (
    """
    An optional argument that specifies if the image is a gif animation
    e.g.
    -gf or --gif
    """
)


REPEAT_ARG_HELP_STRING: str = (
    """
    An optional argument that specifies if the gif animation should be repeated
    e.g.
    -r or --repeat
    """
)

LOGO_PATH = os.path.join(os.path.dirname(__file__), "./logo.ansi")
TEXT_LOGO: str
with open(LOGO_PATH, "r", encoding="utf-8") as logo_file:
    TEXT_LOGO = logo_file.read()

LOGO_DELIMITER_LENGTH = sum(1 for i in TEXT_LOGO.partition('\n')[0]
                                if ord(i) in range(0x2800, 0x28ff + 1))
LOGO_DELIMITER = '-' * LOGO_DELIMITER_LENGTH

sys.stdout.reconfigure(encoding="utf-8")

def _resize_portrait(image: Image, width: int = None):
    if not width:
        width = 100
    wpercent = width / float(image.size[0])
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((width, hsize), Image.Resampling.LANCZOS)
    return image

def _exception_handler(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except GifUnsupportedResizeError:
            logger.error("Error! Gif resizing is not supported.")
        except GifUnsupportedSaveError:
            logger.error("Error! Gif arts saving is not supported.")
        except KeyboardInterrupt:
            pass
        except Exception as error: #pylint: disable = broad-except
            logger.error("Error! Unexpected exception caught:")
            logger.info(str(error))

    return wrapper

#@_exception_handler
def main() -> None:
    """Main function."""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-fp", "--file-path", dest="file_path",
                                        required=True, help=FP_ARG_HELP_STRING)
    argument_parser.add_argument("-m", "--mode", dest="mode", choices=[i.value
                        for i in AvailableColors], default="2", type=str, help=MODE_ARG_HELP_STRING)
    argument_parser.add_argument("-w", "--width", dest="width", type=int, help=MODE_ARG_HELP_STRING)
    argument_parser.add_argument("-o", "--out", dest="out", default=None, help=OUT_ARG_HELP_STRING)
    argument_parser.add_argument("-t", "--threshold", dest="threshold", default=None, type=int,
                                                                    help=THRESHOLD_ARG_HELP_STRING)
    argument_parser.add_argument("-dl", "--disable-logging", action="store_true",
                                                            help=DISABLE_LOGGING_ARG_HELP_STRING)
    argument_parser.add_argument("-gf", "--gif", action="store_true", dest="gif",
                                                        help=GIF_ARG_HELP_STRING)
    argument_parser.add_argument("-r", "--repeat", action="store_true",
                                                        help=REPEAT_ARG_HELP_STRING)

    arguments = argument_parser.parse_args()

    if arguments.disable_logging:
        logger.setLevel(logging.ERROR)
    else:
        print(TEXT_LOGO)
        print(f"Author: {__author__} <{__author_email__}>  Version: {__version__}")
        print(LOGO_DELIMITER)

    logger.info("Generating...")
    image = Image.open(arguments.file_path)
    if not arguments.gif:
        image = _resize_portrait(image, arguments.width)

    generator = Generator(image,
            arguments.mode, threshold=arguments.threshold)

    if arguments.gif:
        if arguments.width:
            raise GifUnsupportedResizeError
        if arguments.out:
            raise GifUnsupportedSaveError
        animation = generator.generate_gif_frames()
    else:
        art = generator.generate_art()

    logger.success("Generated!")
    if arguments.out:
        with open(arguments.out, "w", encoding="utf-8") as out_file:
            out_file.write(art)
        logger.info("Saved to -> %s", arguments.out)
    else:
        if arguments.gif:
            while True:
                for frame in animation.frames:
                    print(frame)
                    sleep(animation.frame_delay)
                if not arguments.repeat:
                    break
        else:
            print(art)
