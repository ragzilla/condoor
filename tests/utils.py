import os
from condoor.connection import _CACHE_FILE


def remove_cache_file():
    try:
        os.remove(_CACHE_FILE)
    except OSError:
        pass

    try:
        os.remove(_CACHE_FILE + '.db')
    except OSError:
        pass
