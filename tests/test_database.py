from sys import path

path.append('../src')

from parts import Part
from holes import Hole
from database import Database
from os import environ

db = Database(environ['databaseURL'])

j = {'name': 'B', 'holes': [{'hole_type': 'circular', 'position': {'quadrant': 0, 'x': 0.191, 'y': 0.507}, 'size': 0.4575786463298379, 'tolerance': 0.2}, {'hole_type': 'circular', 'position': {'quadrant': 0, 'x': 0.763, 'y': 1}, 'size': 0.2669208770257388, 'tolerance': 0.333}, {'hole_type': 'hexagonal', 'position': {'quadrant': 1, 'x': 0.237, 'y': 0.384}, 'size': 0.22878932316491896, 'tolerance': 0.333}, {'hole_type': 'hexagonal', 'position': {'quadrant': 2, 'x': 0.237, 'y': 0.616}, 'size': 0.22878932316491896, 'tolerance': 0.333}, {'hole_type': 'cross', 'position': {'quadrant': 3, 'x': 0, 'y': 0.555}, 'size': 0.22878932316491896, 'tolerance': 0.333}], 'rightCounter': 0, 'wrongCounter': 0}
example_part = Part('1002')
example_part.load_json(j)


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
