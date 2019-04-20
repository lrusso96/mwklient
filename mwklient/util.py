"""The util module provides some common helper functions and wrappers,
to parse timestamps, read streams in chunks, etc.
"""

from io import BytesIO
from time import strptime


def strip_namespace(title):
    if title[0] == ':':
        title = title[1:]
    return title[title.find(':') + 1:]


def normalize_title(title):
    # TODO: Make site dependent
    title = title.strip()
    if title[0] == ':':
        title = title[1:]
    title = title[0].upper() + title[1:]
    title = title.replace(' ', '_')
    return title


def parse_timestamp(timestamp):
    """Parses a string to a time tuple.

    Args:
        timestamp: A string fomrttaed as formatted as '%Y-%m-%dT%H:%M:%SZ'; if
        None, it is considered as '0000-00-00T00:00:00Z'.

    Returns:
        a time tuple (struct_time)

    Raises:
    """
    if not timestamp or timestamp == '0000-00-00T00:00:00Z':
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    return strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')


def read_in_chunks(stream, chunk_size):
    """Reads from a buffer in chunks.

    Args:
        stream: The underlying buffer to read.
        chunk_size: number of characters to read each time; if it is negative,
        the full buffer is read, untile EOF.

    Returns:
        bytes

    Raises:
    """
    while True:
        data = stream.read(chunk_size)
        if not data:
            break
        yield BytesIO(data)
