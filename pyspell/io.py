import re
import gzip
import bz2


SUPPORTED_EXTENSION = re.compile(ur'(\.(?:gz|bz2))$', re.IGNORECASE)


def get_extension(fname, regex=SUPPORTED_EXTENSION, lowercase=True):
    """Return a string containing its extension (if matches pattern)
    """
    match = regex.search(fname)
    if match is None:
        return None
    elif lowercase:
        return match.group().lower()
    else:
        return match.group()


FILEOPEN_FUNCTIONS = {
    '.gz': lambda fname, mode='r', compresslevel=9: gzip.open(fname, mode + 'b', compresslevel),
    '.bz2': lambda fname, mode='r', compresslevel=9: bz2.BZ2File(fname, mode, compresslevel)
}


def open_gz(fname, mode='r', compresslevel=9):
    """Transparent substitute to open() for gzip, bz2 support

    If extension was not found or is not supported, assume it's a plain-text file
    """
    extension = get_extension(fname)
    if extension is None:
        return open(fname, mode)
    else:
        fopen_fun = FILEOPEN_FUNCTIONS[extension]
        return fopen_fun(fname, mode, compresslevel)
