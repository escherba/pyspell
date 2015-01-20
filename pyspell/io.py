import re
import gzip
import bz2
import codecs
from contextlib import contextmanager


SUPPORTED_EXTENSION = re.compile(ur'(\.(?:gz|bz2))$', re.IGNORECASE)


@contextmanager
def passthrough_context(*args):
    """Generic empty context wrapper

    Allows constructions like:
    with passthrough_context(open("filename.txt", "r")) as fhandle:
    with passthrough_context(open("filename.txt", "r"), open("filename.txt", "r")) as (fhanlde1, fhandle2):
    """
    yield args[0] if len(args) == 1 else args


def isiterable(obj):
    """
    Are we being asked to look up a list of things, instead of a single thing?
    We check for the `__iter__` attribute so that this can cover types that
    don't have to be known by this module, such as NumPy arrays.

    Strings, however, should be considered as atomic values to look up, not
    iterables.

    We don't need to check for the Python 2 `unicode` type, because it doesn't
    have an `__iter__` attribute anyway.

    This method was written by Luminoso Technologies
        https://github.com/LuminosoInsight/ordered-set
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


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


def read_text_resource(finput, encoding='utf-8', ignore_prefix='#'):
    """Read a text resource ignoring comments beginning with pound sign
    :param finput: path or file handle
    :type finput: str, file
    :param encoding: which encoding to use (default: UTF-8)
    :type encoding: str
    :param ignore_prefix: lines matching this prefix will be skipped
    :type ignore_prefix: str, unicode
    :rtype: generator
    """
    ctx = passthrough_context(codecs.iterdecode(finput, encoding=encoding)) \
        if isiterable(finput) \
        else codecs.open(finput, 'r', encoding=encoding)
    with ctx as fhandle:
        for line in fhandle:
            if ignore_prefix is not None:
                line = line.split(ignore_prefix)[0]
            line = line.strip()
            if line:
                yield line
