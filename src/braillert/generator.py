from typing import NamedTuple

from PIL import Image, ImageStat, ImageSequence

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

class Animation(NamedTuple):
    """Animation class"""
    frames: tuple
    frame_delay: float

class Generator:
    """Braille art generator class"""
    def __init__(self,
        image: Image,
        palette: dict = None,
        resetter: str = '',
        threshold: int = None
    ) -> None:
        self._image = image
        self._palette = palette
        self._resetter = resetter
        self._threshold = threshold

    def _generate_segment(
        self,
        current_width: int,
        current_height: int
    ) -> str:
        grayscale = self._palette is None
        symbol_relative_pos = 0
        segment_pixels = []
        image = self._image.convert("RGBA")
        image_grayscale = self._image.convert("L")
        for part_height in range(BRAILLE_DOTS_HEIGHT):
            for part_width in range(BRAILLE_DOTS_WIDTH):
                pixel_grayscale = image_grayscale.getpixel((current_width + part_width,
                                                                current_height + part_height))
                pixel = image.getpixel(
                    (current_width + part_width, current_height + part_height))
                segment_pixels.append(pixel)
                if pixel_grayscale > self._threshold:
                    symbol_relative_pos += PIXEL_MAP[part_height][part_width]

        segment = chr(BRAILLE_UNICODE_START + symbol_relative_pos)
        segment_opaque = not any(pixel[RGB_LEN] != 0 for pixel in segment_pixels)
        if not grayscale:
            segment = FULL_BRAILLE_SYMBOL if (symbol_relative_pos == 0
                                    and not segment_opaque) else segment

        color = _get_nearest_color(*[sum(x)/len(x) for x in zip(*segment_pixels)][0:RGB_LEN],
                                                        self._palette) if not grayscale else ''
        return color + segment + self._resetter

    def generate_art(self) -> str:
        """Generates braille art from a picture."""
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
            for _ in range(self._image.width // BRAILLE_DOTS_WIDTH):
                art_string += symbols[count]
                count += 1
            art_string += "\n"

        return art_string

    def generate_gif_frames(
        self
    ) -> Animation:
        """Generates frames from a gif image using generate_art"""
        frames = []
        total_duration: int = 0
        frames_len: int = 0
        for frame in ImageSequence.Iterator(self._image):
            self._image = frame
            frames.append(self.generate_art())
            total_duration += frame.info['duration']
            frames_len += 1
        average_fps = total_duration / frames_len
        return Animation(frames=tuple(frames), frame_delay = 1 / average_fps)
