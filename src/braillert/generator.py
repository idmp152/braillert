import os

from PIL import Image, ImageStat

PIXEL_MAP = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))

BRAILLE_DOTS_HEIGHT = 4
BRAILLE_DOTS_WIDTH = 2
RGB_LEN = 3

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

def _generate_segment(
    image: Image,
    current_width: int,
    current_height: int,
    threshold: int,
    palette: bool,
    resetter: str,
) -> str:
    grayscale = palette is None
    symbol_relative_pos = 0
    segment_pixels = []
    image_grayscale = image.convert("L")
    for part_height in range(BRAILLE_DOTS_HEIGHT):
        for part_width in range(BRAILLE_DOTS_WIDTH):
            pixel_grayscale = image_grayscale.getpixel((current_width + part_width,
                                                            current_height + part_height))
            pixel = image.getpixel((current_width + part_width, current_height + part_height))
            segment_pixels.append(pixel)
            if pixel_grayscale > threshold:
                symbol_relative_pos += PIXEL_MAP[part_height][part_width]

    segment = chr(BRAILLE_UNICODE_START + symbol_relative_pos)
    segment_opaque = not any(pixel[RGB_LEN] != 0 for pixel in segment_pixels)
    if not grayscale:
        segment = FULL_BRAILLE_SYMBOL if (symbol_relative_pos == 0
                                and not segment_opaque) else segment

    color = _get_nearest_color(*[sum(x)/len(x) for x in zip(*segment_pixels)][0:RGB_LEN],
                                                    palette) if not grayscale else ''
    return color + segment + resetter

def generate_art(
    source_path: str | os.PathLike,
    palette: dict = None,
    resetter: str = '',
    threshold: int = None,
    art_width: int = 100
) -> str:
    """Generates braille art from a picture."""
    symbols = []
    image = Image.open(source_path).convert("RGBA")
    image = _resize_portrait(image, art_width)

    if threshold is None:
        threshold = ImageStat.Stat(image.convert("L")).mean[0]

    for height in range(
        0,
        _floor_to_nearest_multiple(image.height, BRAILLE_DOTS_HEIGHT),
        BRAILLE_DOTS_HEIGHT,
    ):
        for width in range(
            0,
            _floor_to_nearest_multiple(image.width, BRAILLE_DOTS_WIDTH),
            BRAILLE_DOTS_WIDTH,
        ):
            symbols.append(_generate_segment(image, width, height, threshold, palette, resetter))

    art_string = ""
    count = 0
    for _ in range(image.height // BRAILLE_DOTS_HEIGHT):
        for _ in range(image.width // BRAILLE_DOTS_WIDTH):
            art_string += symbols[count]
            count += 1
        art_string += "\n"

    return art_string
