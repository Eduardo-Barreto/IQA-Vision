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
        '''
        Construtor da classe Part

        Parâmetros
        ----------
        ID: str
            ID da peça

        name: str
            Nome da peça

        holes: list
            Lista de furos

        rightCounter: int
            Peças corretas contadas

        wrongCounter: int
            Peças erradas contadas

        Examples
        --------
        >>> part = Part('1', 'Part 1', [Hole('circular', {'x': 0, 'y': 0}, 10, 0.1)])
        '''
        self.ID = ID
        self.name = name
        self.holes = holes
        self.rightCounter = rightCounter
        self.wrongCounter = wrongCounter

    def __eq__(self, other) -> bool:
        '''
        Operador de igualdade

        Parâmetros
        ----------
        other: Part
            Peça a ser comparada

        Retorno
        -------
        equal: bool
            True se o json das peças forem iguais, False caso contrário

        Examples
        --------
        >>> part1 = Part('1', 'Part 1', [Hole('circular', {'x': 0, 'y': 0}, 10, 0.1)])
        >>> part2 = Part('1', 'Part 1', [Hole('circular', {'x': 0, 'y': 0}, 10, 0.1)])
        >>> part1 == part2
        True
        '''
        return self.to_json() == other.to_json()

    def to_json(self) -> str:
        '''
        Converte a peça em json

        Retorno
        -------
        ID: str
            ID da peça
        json: str
            Peça em json
        Examples
        --------
        >>> part = Part('1', 'Part 1', [Hole('circular', {'x': 0, 'y': 0}, 10, 0.1)])
        >>> part.to_json()
        ''1', {"name": "Part 1", "holes": [{"hole_type": "circular", "position": {"x": 0, "y": 0}, "size": 10, "tolerance": 0.1}], "rightCounter": 0, "wrongCounter": 0}'
        '''
        return self.ID, dumps({
                "name": self.name,
                "holes": [hole.__dict__ for hole in self.holes],
                "rightCounter": self.rightCounter,
                "wrongCounter": self.wrongCounter
        })

    def load_json(self, json) -> None:
        '''
        Carrega uma peça a partir de um json

        Parâmetros
        ----------
        json: str
            Peça em json

        Examples
        --------
        >>> part = Part('1')
        >>> part.load_json({"name": "Part 1", "holes": [{"hole_type": "circular", "position": {"x": 0, "y": 0}, "size": 10, "tolerance": 0.1}], "rightCounter": 0, "wrongCounter": 0})
        '''
        self.name = json["name"]
        self.holes = [Hole(**hole) for hole in json["holes"]]
        self.rightCounter = json["rightCounter"]
        self.wrongCounter = json["wrongCounter"]
