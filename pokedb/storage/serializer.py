"""Storing rows as tuples. A schema is currently a tuple of field names."""
from itertools import izip


def serialize(schema, deserialized_row):
    serialized_fields = []
    for field in schema:
        serialized_fields.append(deserialized_row[field])
    return tuple(serialized_fields)


def deserialize(schema, serialized_row):
    deserialized_row = dict()
    for field_name, field_value in izip(schema, serialized_row):
        deserialized_row[field_name] = field_value
    return deserialized_row
