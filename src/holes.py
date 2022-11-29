class Hole:
    def __init__(
        self,
        hole_type: str,
        position: dict,
        size: float,
        tolerance: float
    ):
        '''
        Construtor da classe Hole

        Parâmetros
        ----------
        hole_type: str
            Tipo do furo

        position: dict
            quadrante e porcentagem em X e Y do furo

        size: float
            Tamanho do furo

        tolerance: float
            Tolerância do furo

        Exemplos
        --------
        >>> hole = Hole('circular', 1, (0.72, 0.45), 10, 0.2)
        '''
        self.hole_type = hole_type
        self.quadrant = position['quadrant']
        self.position = (position['x'], position['y'])
        self.size = size
        self.tolerance = tolerance

    def to_dict(self):
        '''
        Converte a classe de furo para o padrão json da database

        Retorno
        -------
        hole: dict
            Furo em json

        Exemplos
        --------
        >>> hole = Hole('circular', 1, (0.72, 0.45), 10, 0.2)
        >>> hole.to_dict()
        {
            "hole_type": "circular",
            "position": {
                "quadrant": 1,
                "x": 0.72,
                "y": 0.45
            },
            "size": 10,
            "tolerance": 0.2
        }
        '''
        return {
            "hole_type": self.hole_type,
            "position": {
                "quadrant": self.quadrant,
                "x": self.position[0],
                "y": self.position[1]
            },
            "size": self.size,
            "tolerance": self.tolerance
        }
