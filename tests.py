from sys import path

path.append('./src')

from parts import Part
from holes import Hole
from database import Database
from os import environ

db = Database(environ['databaseURL'])

example_hole = Hole('hexagonal', {'x': 11, 'y': 22}, 2, 0.1)
example_part = Part('9999', 'example_part', [example_hole], 0, 0)


def get_part_by_id():
    assert db.get_part_by_id(example_part.ID) == example_part


def get_part_by_name():
    assert db.get_part_by_name(example_part.name) == example_part


def create_part():
    assert db.create_part(example_part) == 200


def update_part():
    assert db.update_part(example_part) == 200


def delete_part():
    assert db.delete_part(example_part) == 200


def tests():
    print('\nTesting creating part...')
    create_part()
    print('Part created successfully!')
    print('\nTesting getting part by id...')
    get_part_by_id()
    print('Part got successfully!')
    print('\nTesting getting part by name...')
    get_part_by_name()
    print('Part got successfully!')
    print('\nTesting updating part...')
    update_part()
    print('Part updated successfully!')
    print('\nTesting deleting part...')
    delete_part()
    print('Part deleted successfully!')
    print('\nAll tests passed successfully!')


if __name__ == '__main__':
    tests()
