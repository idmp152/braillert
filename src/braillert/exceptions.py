class GifUnsupportedResizeError(Exception):
    """
    Exception is raised when a --width
    option is passed with the -gf flag
    (Gif resize is unsupported)
    """

class GifUnsupportedSaveError(Exception):
    """
    Exception is raised when a --out
    option is passed with the -gf flag
    (Gif save is unsupported)
    """
