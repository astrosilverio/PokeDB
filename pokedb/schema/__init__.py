from pokedb.schema import serializer

SCHEMA_FMT = '32sc?32s'

_table_schema = dict()


def describe(table_name):
    table = _table_schema.get(table, None)
    if not table:
        raise ValueError("Table does not exist")

    cols = []
    for row_id, row in table.iteritems():
        col = serializer.deserialize_from_bits(SCHEMA_FMT, row)
        cols.append(col)

    return col


def get_table_fmt(table_name):
    if table_name == 'schema':
        return SCHEMA_FMT

    cols = describe(table_name)
    col_types = [col[1] for col in cols]
    return ''.join(col_types)


def serialize(table, row):
    fmt = get_table_fmt(table)
    return serializer.serialize_to_bits(fmt, row)


def deserialize(table, raw_data):
    fmt = get_table_fmt(table)
    return serializer.deserialize_from_bits(fmt, raw_data)
