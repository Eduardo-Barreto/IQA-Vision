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
            Posição do furo

        size: float
            Tamanho do furo

        tolerance: float
            Tolerância do furo

        Examples
        --------
        >>> hole = Hole('circular', {'x': 0, 'y': 0}, 10, 0.1)
        '''
        self.hole_type = hole_type
        self.position = position
        self.size = size
        self.tolerance = tolerance
