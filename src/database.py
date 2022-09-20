from parts import Part
import requests
from json import dumps


class Database:
    def __init__(self, url):
        self.url = url

    def _part_to_json(self, part: Part):
        part_id = part.ID
        part = part.__dict__
        part["holes"] = [hole.__dict__ for hole in part["holes"]]
        part.pop("ID")
        return part_id, dumps(part)

    def part_exists(self, part_id: int):
        link = requests.get(f'{self.url}/parts/{part_id}/.json')
        return link.status_code == 200 and link.json() is not None

    def get_part_by_id(self, part_id: int):
        get_request = requests.get(f'{self.url}/parts/{part_id}/.json')
        part = Part(part_id)
        part.load_json(get_request.json())
        return part

    def get_part_by_name(self, name: str):
        get_request = requests.get(f'{self.url}/parts/.json')
        for part_id, part in get_request.json().items():
            if part["name"] == name:
                return self.get_part_by_id(part_id)

    def create_part(self, part: Part):
        part_id, part = part.to_json()

        create_request = requests.put(
            f'{self.url}/parts/{part_id}/.json', data=part
        )
        return create_request.status_code

    def update_part(self, part: Part):
        part_id, part = part.to_json()

        update_request = requests.patch(
            f'{self.url}/parts/{part_id}/.json', data=part
        )
        return update_request.status_code

    def delete_part(self, part: Part):
        part_id, part = part.to_json()

        delete_request = requests.delete(
            f'{self.url}/parts/{part_id}/.json')

        return delete_request.status_code
