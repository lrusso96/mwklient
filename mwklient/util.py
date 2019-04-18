from io import BytesIO
from time import strptime


def parse_timestamp(timestamp):
    if not timestamp or timestamp == '0000-00-00T00:00:00Z':
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    return strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')


def read_in_chunks(stream, chunk_size):
    while True:
        data = stream.read(chunk_size)
        if not data:
            break
        yield BytesIO(data)
