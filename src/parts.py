from json import dumps
from holes import Hole


class Part:
    def __init__(
        self,
        ID: str,
        name: str = '',
        holes: list = [],
        rightCounter: int = 0,
        wrongCounter: int = 0
    ):
        self.ID = ID
        self.name = name
        self.holes = holes
        self.rightCounter = rightCounter
        self.wrongCounter = wrongCounter

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def to_json(self):
        return self.ID, dumps({
                "name": self.name,
                "holes": [hole.__dict__ for hole in self.holes],
                "rightCounter": self.rightCounter,
                "wrongCounter": self.wrongCounter
        })

    def load_json(self, json):
        self.name = json["name"]
        self.holes = [Hole(**hole) for hole in json["holes"]]
        self.rightCounter = json["rightCounter"]
        self.wrongCounter = json["wrongCounter"]
