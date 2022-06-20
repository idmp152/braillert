import os

from PIL import Image, ImageEnhance, ImageStat
from colorama import Style

from braillert.colors import ColorTypes, RICH_COLORS, COLORAMA_COLORS, DISCORD_COLORS


PIXEL_MAP = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))

BRAILLE_DOTS_HEIGHT = 4
BRAILLE_DOTS_WIDTH = 2

BRAILLE_UNICODE_START = 0x2800
FULL_BRAILLE_SYMBOL = '\u28ff'


def _get_nearest_color(red: float, green: float, blue: float, pallete: dict) -> str:
    return pallete[min(pallete.keys(), key=lambda color: sum((abs(
                red - color[0]), abs(green - color[1]), abs(blue - color[2])))/3)]


def _floor_to_nearest_multiple(number: int, multiple: int) -> int:
    return (number // multiple) * multiple


def _resize_portrait(image: Image, width: int):
    wpercent = width / float(image.size[0])
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((width, hsize), Image.Resampling.LANCZOS)
    return image

def _get_pallete_dict_by_type(pallete_type: ColorTypes) -> dict | None:
    if pallete_type == ColorTypes.RICH:
        return RICH_COLORS
    if pallete_type == ColorTypes.COLORAMA:
        return COLORAMA_COLORS
    if pallete_type == ColorTypes.DISCORD:
        return DISCORD_COLORS
    if pallete_type == ColorTypes.GRAYSCALE:
        return
    raise Exception()

def _get_resetter_by_pallete_type(pallete_type: ColorTypes) -> str | None:
    if pallete_type == ColorTypes.RICH:
        return "[/]"
    if pallete_type == ColorTypes.COLORAMA:
        return Style.RESET_ALL
    if pallete_type == ColorTypes.DISCORD:
        return
    if pallete_type == ColorTypes.GRAYSCALE:
        return
    raise Exception()

def generate_art(
    source_path: str | os.PathLike,
    pallete_type: ColorTypes,
    threshold: int = None,
    art_width: int = 100,
    contrast: float = None
) -> str:
    """Generates braille art from a picture."""
    grayscale = pallete_type == ColorTypes.GRAYSCALE
    pallete = _get_pallete_dict_by_type(pallete_type)
    resetter = _get_resetter_by_pallete_type(pallete_type) or ''
    symbols = []
    image = Image.open(source_path).convert("RGB")
    image = _resize_portrait(image, art_width)

    image_grayscale = image.convert("L")
    if contrast is not None:
        image_grayscale = ImageEnhance.Contrast(image_grayscale).enhance(contrast)

    if threshold is None:
        threshold = ImageStat.Stat(image_grayscale).mean[0]

    for height in range(
        0,
        _floor_to_nearest_multiple(image_grayscale.height, BRAILLE_DOTS_HEIGHT),
        BRAILLE_DOTS_HEIGHT,
    ):
        for width in range(
            0,
            _floor_to_nearest_multiple(image_grayscale.width, BRAILLE_DOTS_WIDTH),
            BRAILLE_DOTS_WIDTH,
        ):
            symbol_relative_pos = 0
            segment_pixels = []
            for part_height in range(BRAILLE_DOTS_HEIGHT):
                for part_width in range(BRAILLE_DOTS_WIDTH):
                    pixel_grayscale = image_grayscale.getpixel((width + part_width,
                                                                    height + part_height))
                    pixel = image.getpixel((width + part_width, height + part_height))
                    segment_pixels.append(pixel)
                    if pixel_grayscale > threshold:
                        symbol_relative_pos += PIXEL_MAP[part_height][part_width]

            segment = chr(BRAILLE_UNICODE_START + symbol_relative_pos)
            if not grayscale:
                segment = FULL_BRAILLE_SYMBOL if symbol_relative_pos == 0 else segment

            color = _get_nearest_color(*[sum(x)/len(x) for x in zip(*segment_pixels)],
                                                            pallete) if not grayscale else ''
            symbols.append(color + segment + resetter)

    art_string = ""
    count = 0
    for _ in range(image_grayscale.height // BRAILLE_DOTS_HEIGHT):
        for _ in range(image_grayscale.width // BRAILLE_DOTS_WIDTH):
            art_string += symbols[count]
            count += 1
        art_string += "\n"

    return art_string
