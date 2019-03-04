import unittest

from pokedb.storage import serializer


class TestSerialize(unittest.TestCase):

    def test_raises_if_deserialized_row_is_missing_fields(self):
        fmt = 'H32s32s32s'
        deserialized_row = (1, 'bulbasaur', 'poison')
        with self.assertRaises(ValueError):
            serializer.serialize(fmt, deserialized_row)

    def test_raises_if_deserialized_row_has_fields_of_incorrect_types(self):
        fmt = 'H32s32s32s'
        deserialized_row = ('bulbasaur', 'grass', 'poison', 1)
        with self.assertRaises(ValueError):
            serializer.serialize(fmt, deserialized_row)


class TestTupleSerialize(unittest.TestCase):

    def test_raises_if_deserialized_row_is_missing_field(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        deserialized_row = {
            'id': 1,
            'name': 'bulbasaur',
            'secondary type': 'poison',
        }
        with self.assertRaises(KeyError):
            serializer.tuple_serialize(schema, deserialized_row)

    def test_returns_fields_in_appropriate_order(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        deserialized_row = {
            'id': 1,
            'name': 'bulbasaur',
            'primary type': 'grass',
            'secondary type': 'poison',
        }

        raw_data = serializer.tuple_serialize(schema, deserialized_row)
        self.assertEqual(raw_data, (1, 'bulbasaur', 'grass', 'poison'))


class TestDeserialize(unittest.TestCase):

    def test_raises_if_row_serialized_with_missing_fields(self):
        fmt = 'H10s10s10s'
        serialized_row = '\x01\x00bulbasaur\x00grass\x00\x00\x00\x00\x00'
        with self.assertRaises(ValueError):
            serializer.deserialize(fmt, serialized_row)

    def test_returns_tuples_of_parsed_fields(self):
        fmt = 'H10s10s10s'
        serialized_row = '\x10\x00pidgey\x00\x00\x00\x00normal\x00\x00\x00\x00flying\x00\x00\x00\x00'

        data = serializer.deserialize(fmt, serialized_row)
        expected_data = (16, 'pidgey', 'normal', 'flying')
        self.assertEqual(data, expected_data)


class TestTupleDeserialize(unittest.TestCase):

    def test_raises_if_row_serialized_with_incorrect_fields(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        serialized_row = ('bulbasaur', 'poison')

        with self.assertRaises(ValueError):
            serializer.tuple_deserialize(schema, serialized_row)

    def test_returns_fields_in_dictionary_form(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        serialized_row = (16, 'pidgey', 'normal', 'flying')

        data = serializer.tuple_deserialize(schema, serialized_row)
        expected_data = {
            'id': 16,
            'name': 'pidgey',
            'primary type': 'normal',
            'secondary type': 'flying',
        }

        self.assertEqual(data, expected_data)
