from typing import NamedTuple

from PIL import Image, ImageSequence, ImageStat

from braillert.colors import AvailableColors, ANSI_RESETTER, closest_ansi_string

PIXEL_MAP = ((0x01, 0x08), (0x02, 0x10), (0x04, 0x20), (0x40, 0x80))

BRAILLE_DOTS_HEIGHT = 4
BRAILLE_DOTS_WIDTH = 2
RGB_LEN = 3

BRAILLE_UNICODE_START = 0x2800
FULL_BRAILLE_SYMBOL = '\u28ff'


def _floor_to_nearest_multiple(number: int, multiple: int) -> int:
    return (number // multiple) * multiple

def _get_grayscale(red: int, green: int, blue: int) -> float:
    return red * 299/1000 + green * 587/1000 + blue * 114/1000

class Frame(NamedTuple):
    """Animation class"""
    content: str
    frame_delay_ms: int

class Generator:
    """Braille art generator class"""
    def __init__(self,
        image: Image,
        palette: AvailableColors = AvailableColors.GRAYSCALE,
        threshold: int = None
    ) -> None:
        self._image = image
        self._palette = palette
        self._resetter = '' if palette == AvailableColors.GRAYSCALE else ANSI_RESETTER
        self._threshold = threshold

    def _generate_segment(
        self,
        current_width: int,
        current_height: int
    ) -> str:
        grayscale = self._palette == AvailableColors.GRAYSCALE
        symbol_relative_pos = 0
        segment_pixels = []
        for part_height in range(BRAILLE_DOTS_HEIGHT):
            for part_width in range(BRAILLE_DOTS_WIDTH):
                pixel = self._image.getpixel(
                    (current_width + part_width, current_height + part_height))
                pixel_grayscale = _get_grayscale(*pixel[0:3])
                segment_pixels.append(pixel)
                if pixel_grayscale > self._threshold:
                    symbol_relative_pos += PIXEL_MAP[part_height][part_width]

        segment = chr(BRAILLE_UNICODE_START + symbol_relative_pos)
        segment_opaque = not any(pixel[RGB_LEN] != 0 for pixel in segment_pixels)
        if not grayscale:
            segment = FULL_BRAILLE_SYMBOL if (symbol_relative_pos == 0
                                    and not segment_opaque) else segment

        color = closest_ansi_string(*[sum(x)/len(x) for x in zip(*segment_pixels)][0:RGB_LEN],
                                                            self._palette) if not grayscale else ''
        return color + segment

    def generate_art(self) -> str:
        """Generates braille art from a picture."""
        self._image = self._image.convert("RGBA")
        symbols = []

        if self._threshold is None:
            self._threshold = ImageStat.Stat(self._image.convert("L")).mean[0]

        for height in range(
            0,
            _floor_to_nearest_multiple(self._image.height, BRAILLE_DOTS_HEIGHT),
            BRAILLE_DOTS_HEIGHT,
        ):
            for width in range(
                0,
                _floor_to_nearest_multiple(self._image.width, BRAILLE_DOTS_WIDTH),
                BRAILLE_DOTS_WIDTH,
            ):
                symbols.append(self._generate_segment(width, height))

        art_string = ""
        count = 0
        for _ in range(self._image.height // BRAILLE_DOTS_HEIGHT):
            art_string += "\n"
            for _ in range(self._image.width // BRAILLE_DOTS_WIDTH):
                art_string += symbols[count]
                count += 1

        return art_string + self._resetter

    def generate_gif_frames(
        self
    ) -> tuple[Frame]:
        """Generates frames from a gif image using generate_art"""
        frames = []
        for frame in ImageSequence.Iterator(self._image):
            self._image = frame
            frames.append(Frame(self.generate_art(), frame.info['duration']))
        return tuple(frames)
