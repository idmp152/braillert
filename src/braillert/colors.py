""" https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797 """
from itertools import product
from enum import Enum

ESC: str = "\u001b"
FOREGROUND: str = "[38;5;"
ANSI_RESETTER: str = ESC + "[0m"

LOW_8_COLORS: tuple = ((0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
                        (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192))

HIGH_8_COLORS: tuple = ((128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                        (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255))
LOW_8_COLORS_DICT: dict = {str(i): LOW_8_COLORS[i] for i in range(8)}
HIGH_8_COLORS_DICT: dict = {str(i + 8): HIGH_8_COLORS[i] for i in range(8)}

EXTENDED_GRAYSCALE_COLORS: tuple = tuple((int(i*(256 / 24)),)*3 for i in range(1,24+1))

COLOR_MATRIX_INCREMENTS = range(95, 256, 40)

ANSI_BASIC_16_DICT: dict = {**LOW_8_COLORS_DICT, **HIGH_8_COLORS_DICT}

COLOR_CUBE_MATRIX: dict = list(product(*([[0] + list(COLOR_MATRIX_INCREMENTS)] * 3)))

ANSI_216_DICT: dict = {str(i + 16): COLOR_CUBE_MATRIX[i] for i in range(216)}

ANSI_24_GRAYSCALE_DICT: dict = {str(i + 216 + 16): EXTENDED_GRAYSCALE_COLORS[i] for i in range(24)}

ANSI_256_DICT: dict = {**ANSI_BASIC_16_DICT, **ANSI_216_DICT, **ANSI_24_GRAYSCALE_DICT}

class AvailableColors(str, Enum):
    """Available colors enum."""
    GRAYSCALE = "2"
    LOW_8_COLORS = "8_lo"
    HIGH_8_COLORS = "8_hi"
    FULL_16_COLORS = "16"
    FULL_SPECTRE = "256"
    GRAYSCALE_EXTENDED = "gs_ext"

def _closest_ansi(red: int, green: int, blue: int, ansi_dict: dict) -> str:
    """
    Closest acceptable ANSI value calculating algorithm.
    """
    return min(ansi_dict.items(), key=lambda x: sum(
        (abs(x[1][0] - red), abs(x[1][1] - green), abs(x[1][2] - blue))))[0]

LOW_8_COLORS_DICT = dict(tuple(ANSI_BASIC_16_DICT.items())[:8])
ansi_dicts: dict = {
    AvailableColors.LOW_8_COLORS: LOW_8_COLORS_DICT,
    AvailableColors.HIGH_8_COLORS: HIGH_8_COLORS_DICT,
    AvailableColors.FULL_16_COLORS: ANSI_BASIC_16_DICT,
    AvailableColors.FULL_SPECTRE: ANSI_256_DICT,
    AvailableColors.GRAYSCALE_EXTENDED: ANSI_24_GRAYSCALE_DICT
}

def closest_ansi_string(red: int, green: int, blue: int, colors: AvailableColors) -> str:
    """
    Closest ANSI value for the given RGB.
    """
    return ESC + FOREGROUND + _closest_ansi(red, green, blue, ansi_dicts[colors]) + "m"
