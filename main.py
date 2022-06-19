import os
import sys

from PIL import Image, ImageEnhance, ImageStat
from rich.console import Console

PIXEL_MAP = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))

BRAILLE_DOTS_HEIGHT = 4
BRAILLE_DOTS_WIDTH = 2

BRAILLE_UNICODE_START = 0x2800

RGB_COLORS = {
    (255, 0, 0): "[bright_red]",
    (0, 0, 0): "[black]",
    (0, 255, 0): "[bright_green]",
    (255, 255, 0): "[bright_yellow]",
    (0, 0, 255): "[bright_blue]",
    (255, 0, 255): "[bright_magenta]",
    (0, 255, 255): "[bright_cyan]",
    (255, 255, 255): "[bright_white]",
    (26, 17, 16): "[bright_black]",
    (139, 0, 0): "[red]",
    (0, 139, 0): "[green]",
    (139, 139, 0): "[yellow]",
    (0, 0, 139): "[blue]",
    (139, 0, 139): "[magenta]",
    (0, 139, 139): "[cyan]",
    (139, 139, 139): "[white]",
    (0, 0, 0): "[grey0]",
    (0, 0, 95): "[navy_blue]",
    (0, 0, 135): "[dark_blue]",
    (0, 0, 215): "[blue3]",
    (0, 0, 255): "[blue1]",
    (0, 95, 0): "[dark_green]",
    (0, 95, 175): "[deep_sky_blue4]",
    (0, 95, 215): "[dodger_blue3]",
    (0, 95, 255): "[dodger_blue2]",
    (0, 135, 0): "[green4]",
    (0, 135, 95): "[spring_green4]",
    (0, 135, 135): "[turquoise4]",
    (0, 135, 215): "[deep_sky_blue3]",
    (0, 135, 255): "[dodger_blue1]",
    (0, 175, 135): "[dark_cyan]",
    (0, 175, 175): "[light_sea_green]",
    (0, 175, 215): "[deep_sky_blue2]",
    (0, 175, 255): "[deep_sky_blue1]",
    (0, 215, 0): "[green3]",
    (0, 215, 95): "[spring_green3]",
    (0, 215, 175): "[cyan3]",
    (0, 215, 215): "[dark_turquoise]",
    (0, 215, 255): "[turquoise2]",
    (0, 255, 0): "[green1]",
    (0, 255, 95): "[spring_green2]",
    (0, 255, 135): "[spring_green1]",
    (0, 255, 175): "[medium_spring_green]",
    (0, 255, 215): "[cyan2]",
    (0, 255, 255): "[cyan1]",
    (95, 0, 175): "[purple4]",
    (95, 0, 215): "[purple3]",
    (95, 0, 255): "[blue_violet]",
    (95, 95, 95): "[grey37]",
    (95, 95, 135): "[medium_purple4]",
    (95, 95, 215): "[slate_blue3]",
    (95, 95, 255): "[royal_blue1]",
    (95, 135, 0): "[chartreuse4]",
    (95, 135, 135): "[pale_turquoise4]",
    (95, 135, 175): "[steel_blue]",
    (95, 135, 215): "[steel_blue3]",
    (95, 135, 255): "[cornflower_blue]",
    (95, 175, 95): "[dark_sea_green4]",
    (95, 175, 175): "[cadet_blue]",
    (95, 175, 215): "[sky_blue3]",
    (95, 215, 0): "[chartreuse3]",
    (95, 215, 135): "[sea_green3]",
    (95, 215, 175): "[aquamarine3]",
    (95, 215, 215): "[medium_turquoise]",
    (95, 215, 255): "[steel_blue1]",
    (95, 255, 95): "[sea_green2]",
    (95, 255, 175): "[sea_green1]",
    (95, 255, 255): "[dark_slate_gray2]",
    (135, 0, 0): "[dark_red]",
    (135, 0, 175): "[dark_magenta]",
    (135, 95, 0): "[orange4]",
    (135, 95, 95): "[light_pink4]",
    (135, 95, 135): "[plum4]",
    (135, 95, 215): "[medium_purple3]",
    (135, 95, 255): "[slate_blue1]",
    (135, 135, 95): "[wheat4]",
    (135, 135, 135): "[grey53]",
    (135, 135, 175): "[light_slate_grey]",
    (135, 135, 215): "[medium_purple]",
    (135, 135, 255): "[light_slate_blue]",
    (135, 175, 0): "[yellow4]",
    (135, 175, 135): "[dark_sea_green]",
    (135, 175, 215): "[light_sky_blue3]",
    (135, 175, 255): "[sky_blue2]",
    (135, 215, 0): "[chartreuse2]",
    (135, 215, 135): "[pale_green3]",
    (135, 215, 215): "[dark_slate_gray3]",
    (135, 215, 255): "[sky_blue1]",
    (135, 255, 0): "[chartreuse1]",
    (135, 255, 135): "[light_green]",
    (135, 255, 215): "[aquamarine1]",
    (135, 255, 255): "[dark_slate_gray1]",
    (175, 0, 95): "[deep_pink4]",
    (175, 0, 135): "[medium_violet_red]",
    (175, 0, 215): "[dark_violet]",
    (175, 0, 255): "[purple]",
    (175, 95, 175): "[medium_orchid3]",
    (175, 95, 215): "[medium_orchid]",
    (175, 135, 0): "[dark_goldenrod]",
    (175, 135, 135): "[rosy_brown]",
    (175, 135, 175): "[grey63]",
    (175, 135, 215): "[medium_purple2]",
    (175, 135, 255): "[medium_purple1]",
    (175, 175, 95): "[dark_khaki]",
    (175, 175, 135): "[navajo_white3]",
    (175, 175, 175): "[grey69]",
    (175, 175, 215): "[light_steel_blue3]",
    (175, 175, 255): "[light_steel_blue]",
    (175, 215, 95): "[dark_olive_green3]",
    (175, 215, 135): "[dark_sea_green3]",
    (175, 215, 215): "[light_cyan3]",
    (175, 215, 255): "[light_sky_blue1]",
    (175, 255, 0): "[green_yellow]",
    (175, 255, 95): "[dark_olive_green2]",
    (175, 255, 135): "[pale_green1]",
    (175, 255, 175): "[dark_sea_green2]",
    (175, 255, 255): "[pale_turquoise1]",
    (215, 0, 0): "[red3]",
    (215, 0, 135): "[deep_pink3]",
    (215, 0, 215): "[magenta3]",
    (215, 95, 0): "[dark_orange3]",
    (215, 95, 95): "[indian_red]",
    (215, 95, 135): "[hot_pink3]",
    (215, 95, 175): "[hot_pink2]",
    (215, 95, 215): "[orchid]",
    (215, 135, 0): "[orange3]",
    (215, 135, 95): "[light_salmon3]",
    (215, 135, 135): "[light_pink3]",
    (215, 135, 175): "[pink3]",
    (215, 135, 215): "[plum3]",
    (215, 135, 255): "[violet]",
    (215, 175, 0): "[gold3]",
    (215, 175, 95): "[light_goldenrod3]",
    (215, 175, 135): "[tan]",
    (215, 175, 175): "[misty_rose3]",
    (215, 175, 215): "[thistle3]",
    (215, 175, 255): "[plum2]",
    (215, 215, 0): "[yellow3]",
    (215, 215, 95): "[khaki3]",
    (215, 215, 175): "[light_yellow3]",
    (215, 215, 215): "[grey84]",
    (215, 215, 255): "[light_steel_blue1]",
    (215, 255, 0): "[yellow2]",
    (215, 255, 135): "[dark_olive_green1]",
    (215, 255, 175): "[dark_sea_green1]",
    (215, 255, 215): "[honeydew2]",
    (215, 255, 255): "[light_cyan1]",
    (255, 0, 0): "[red1]",
    (255, 0, 95): "[deep_pink2]",
    (255, 0, 175): "[deep_pink1]",
    (255, 0, 215): "[magenta2]",
    (255, 0, 255): "[magenta1]",
    (255, 95, 0): "[orange_red1]",
    (255, 95, 135): "[indian_red1]",
    (255, 95, 215): "[hot_pink]",
    (255, 95, 255): "[medium_orchid1]",
    (255, 135, 0): "[dark_orange]",
    (255, 135, 95): "[salmon1]",
    (255, 135, 135): "[light_coral]",
    (255, 135, 175): "[pale_violet_red1]",
    (255, 135, 215): "[orchid2]",
    (255, 135, 255): "[orchid1]",
    (255, 175, 0): "[orange1]",
    (255, 175, 95): "[sandy_brown]",
    (255, 175, 135): "[light_salmon1]",
    (255, 175, 175): "[light_pink1]",
    (255, 175, 215): "[pink1]",
    (255, 175, 255): "[plum1]",
    (255, 215, 0): "[gold1]",
    (255, 215, 135): "[light_goldenrod2]",
    (255, 215, 175): "[navajo_white1]",
    (255, 215, 215): "[misty_rose1]",
    (255, 215, 255): "[thistle1]",
    (255, 255, 0): "[yellow1]",
    (255, 255, 95): "[light_goldenrod1]",
    (255, 255, 135): "[khaki1]",
    (255, 255, 175): "[wheat1]",
    (255, 255, 215): "[cornsilk1]",
    (255, 255, 255): "[grey100]",
    (8, 8, 8): "[grey3]",
    (18, 18, 18): "[grey7]",
    (28, 28, 28): "[grey11]",
    (38, 38, 38): "[grey15]",
    (48, 48, 48): "[grey19]",
    (58, 58, 58): "[grey23]",
    (68, 68, 68): "[grey27]",
    (78, 78, 78): "[grey30]",
    (88, 88, 88): "[grey35]",
    (98, 98, 98): "[grey39]",
    (108, 108, 108): "[grey42]",
    (118, 118, 118): "[grey46]",
    (128, 128, 128): "[grey50]",
    (138, 138, 138): "[grey54]",
    (148, 148, 148): "[grey58]",
    (158, 158, 158): "[grey62]",
    (168, 168, 168): "[grey66]",
    (178, 178, 178): "[grey70]",
    (188, 188, 188): "[grey74]",
    (198, 198, 198): "[grey78]",
    (208, 208, 208): "[grey82]",
    (218, 218, 218): "[grey85]",
    (228, 228, 228): "[grey89]",
    (238, 238, 238): "[grey93]",
}


def get_nearest_color(red: float, green: float, blue: float) -> str:
    """Gets nearest colorama color"""
    return RGB_COLORS[min(RGB_COLORS.keys(), key=lambda color: sum((abs(
                red - color[0]), abs(green - color[1]), abs(blue - color[2])))/3)]


def _floor_to_nearest_multiple(number: int, multiple: int):
    return (number // multiple) * multiple


def _resize_portrait(image: Image, width: int):
    wpercent = width / float(image.size[0])
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((width, hsize), Image.Resampling.LANCZOS)
    return image


def generate_art(
    source_path: str | os.PathLike,
    threshold: int = None,
    art_width: int = 100,
    contrast: float = None,
) -> str:
    """Generates braille art from a picture."""
    symbols = []
    image = Image.open(source_path)
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
            segment = '\u28ff' if symbol_relative_pos == 0 else chr(BRAILLE_UNICODE_START + symbol_relative_pos)
            symbols.append(get_nearest_color(*[sum(x)/len(x) for x in zip(*segment_pixels)])
                            + segment + '[/]')

    art_string = ""
    count = 0
    for _ in range(image_grayscale.height // BRAILLE_DOTS_HEIGHT):
        for _ in range(image_grayscale.width // BRAILLE_DOTS_WIDTH):
            art_string += symbols[count]
            count += 1
        art_string += "\n"

    return art_string


sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

Console().print(generate_art("test.jpg"))
