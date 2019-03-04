"""Storing rows as tuples. A schema is currently a tuple of field names."""
from itertools import izip
import ctypes
import re
import struct

_string_types = ['c', 'b', 'B', 's', 'p']


def serialize(fmt, *deserialized_row):
    try:
        row = struct.pack(fmt, *deserialized_row)
    except struct.error as e:
        raise ValueError(e.message)
    else:
        return row


def deserialize(fmt, serialized_row):
    try:
        row = struct.unpack(fmt, serialized_row)
    except struct.error as e:
        raise ValueError(e.message)

    string_indexes = _find_strings(fmt)
    if string_indexes:
        transform_row = list(row)
        for i, item in enumerate(transform_row):
            if i in string_indexes:
                item = ctypes.create_string_buffer(item).value
                transform_row[i] = item
        row = tuple(transform_row)

    return row


def tuple_serialize(schema, deserialized_row):
    serialized_fields = []
    for field in schema:
        serialized_fields.append(deserialized_row[field])
    return tuple(serialized_fields)


def tuple_deserialize(schema, serialized_row):
    deserialized_row = dict()
    if len(schema) != len(serialized_row):
        raise ValueError('data has been serialized weirdly')
    for field_name, field_value in izip(schema, serialized_row):
        deserialized_row[field_name] = field_value
    return deserialized_row


def _find_strings(fmt_string):
    parts = re.findall('[^A-Za-z]*[A-Za-z]', fmt_string)
    return [i for i, part in enumerate(parts) if part[-1] in _string_types]
