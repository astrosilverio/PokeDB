import unittest

from pokedb.storage import serializer


class TestSerialize(unittest.TestCase):

    def test_raises_if_deserialized_row_is_missing_field(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        deserialized_row = {
            'id': 1,
            'name': 'bulbasaur',
            'secondary type': 'poison',
        }
        with self.assertRaises(KeyError):
            serializer.serialize(schema, deserialized_row)

    def test_returns_fields_in_appropriate_order(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        deserialized_row = {
            'id': 1,
            'name': 'bulbasaur',
            'primary type': 'grass',
            'secondary type': 'poison',
        }

        raw_data = serializer.serialize(schema, deserialized_row)
        self.assertEqual(raw_data, (1, 'bulbasaur', 'grass', 'poison'))


class TestDeserialize(unittest.TestCase):

    def test_raises_if_row_serialized_with_incorrect_fields(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        serialized_row = ('bulbasaur', 'poison')

        with self.assertRaises(ValueError):
            serializer.deserialize(schema, serialized_row)

    def test_returns_fields_in_dictionary_form(self):
        schema = ('id', 'name', 'primary type', 'secondary type')
        serialized_row = (16, 'pidgey', 'normal', 'flying')

        data = serializer.deserialize(schema, serialized_row)
        expected_data = {
            'id': 16,
            'name': 'pidgey',
            'primary type': 'normal',
            'secondary type': 'flying',
        }

        self.assertEqual(data, expected_data)
