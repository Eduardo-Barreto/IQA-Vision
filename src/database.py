from parts import Part
import requests


class Database:
    def __init__(self, url: str) -> None:
        '''
        Construtor da classe Database

        Parâmetros
        ----------
        url: str
            URL do banco de dados

        Exemplos
        --------
        >>> db = Database('https://my-database.firebaseio.com')
        '''
        self.url = url

    def part_exists(self, part_id: str) -> bool:
        '''
        Verifica se uma peça existe no banco de dados

        Parâmetros
        ----------
        part_id: str
            ID da peça

        Retorno
        -------
        exists: bool
            True se a peça existe, False caso contrário

        Exemplos
        --------
        >>> db.part_exists('1')
        True
        '''
        link = requests.get(f'{self.url}/parts/{part_id}/.json')
        return link.status_code == 200 and link.json() is not None

    def get_part_by_id(self, part_id: str) -> Part:
        '''
        Retorna uma peça no banco de dados pelo seu ID

        Parâmetros
        ----------
        part_id: str
            ID da peça

        Retorno
        -------
        part: Part
            Peça

        Exemplos
        --------
        >>> db.get_part_by_id('1')
        Part(ID='1', name='Part 1', holes=[], rightCounter=0, wrongCounter=0)
        '''
        get_request = requests.get(f'{self.url}/parts/{part_id}/.json')
        part = Part(part_id)
        part.load_json(get_request.json())
        return part

    def get_part_by_name(self, name: str) -> Part:
        '''
        Retorna uma peça no banco de dados pelo seu nome

        Parâmetros
        ----------
        name: str
            Nome da peça

        Retorno
        -------
        part: Part
            Peça

        Exemplos
        --------
        >>> db.get_part_by_name('Part 1')
        Part(ID='1', name='Part 1', holes=[], rightCounter=0, wrongCounter=0)
        '''
        get_request = requests.get(f'{self.url}/parts/.json')
        for part_id, part in get_request.json().items():
            if part["name"] == name:
                return self.get_part_by_id(part_id)

        return Part('')

    def create_part(self, part: Part) -> int:
        '''
        Cria uma peça no banco de dados

        Parâmetros
        ----------
        part: Part
            Peça a ser criada

        Retorno
        -------
        status_code: int
            Código HTTP de status da requisição

        Exemplos
        --------
        >>> db.create_part(Part(1, 'Part 1'))
        200
        '''
        part_id, part = part.to_json()

        create_request = requests.put(
            f'{self.url}/parts/{part_id}/.json', data=part
        )
        return create_request.status_code

    def update_part(self, part: Part) -> int:
        '''
        Atualiza uma peça no banco de dados

        Parâmetros
        ----------
        part: Part
            Peça a ser atualizada

        Retorno
        -------
        status_code: int
            Código HTTP de status da requisição

        Exemplos
        --------
        >>> db.update_part(Part(1, 'Part 1'))
        200
        '''
        part_id, part = part.to_json()

        update_request = requests.patch(
            f'{self.url}/parts/{part_id}/.json', data=part
        )
        return update_request.status_code

    def delete_part(self, part: Part) -> int:
        '''
        Deleta uma peça no banco de dados

        Parâmetros
        ----------
        part: Part
            Peça a ser deletada

        Retorno
        -------
        status_code: int
            Código HTTP de status da requisição

        Exemplos
        --------
        >>> db.delete_part(Part(1, 'Part 1'))
        200
        '''
        part_id, part = part.to_json()

        delete_request = requests.delete(
            f'{self.url}/parts/{part_id}/.json')

        return delete_request.status_code
