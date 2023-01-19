import cv2 as cv
from parts import Part
from holes import Hole

from hole_classification import predict_hole_type


class PartImage:
    def __init__(
        self,
        original_image: cv.Mat,
        triangles: list,
        part: Part,
        pencil: bool = False
    ):
        '''
        Construtor da classe PartImage

        Parâmetros
        ----------
        original_image: str
            Caminho da imagem

        triangles: list
            Lista de triângulos

        part: Part
            Peça a ser analisada

        pencil: bool
            Pincel de desenho
        '''
        self.pencil = pencil
        self.original_image = original_image

        self.image = original_image.copy()
        self.draw = original_image.copy()

        self.a, self.b, self.c, self.d = self.sort_triangles(triangles)
        self.triangles = self.a, self.b, self.c, self.d

        self.part = part
        self.calcule_all()

    def proximity(self, value, target, error=0.5):
        '''
        Verifica se um valor está próximo de um alvo

        Parâmetros
        ----------
        value: int
            Valor a ser verificado

        target: int
            Valor alvo

        error: float
            Erro permitido

        Retorno
        -------
        bool
            True se o valor está próximo do alvo
        '''
        return (
            value > (target * (1 - error)) and
            value < (target * (1 + error))
        )


    def sort_triangles(self, triangles: list) -> list:
        sorted_x = sorted(triangles, key=lambda x: x[0])
        sorted_y = sorted(triangles, key=lambda x: x[1])

        larger_x = sorted_x[-2:]
        larger_y = sorted_y[-2:]

        a, b, c, d = 0, 0, 0, 0

        for item in triangles:
            if item in larger_x:
                if item in larger_y:
                    c = item
                    continue
                else:
                    b = item
                    continue

            if item in larger_y:
                d = item
                continue
            else:
                a = item

        return [a, b, c, d]

    def calcule_all(self):
        self.lineAB = (self.a, self.b)
        self.lineBC = (self.b, self.c)
        self.lineCD = (self.c, self.d)
        self.lineDA = (self.d, self.a)

        self.lineAC = (self.a, self.c)
        self.lineBD = (self.b, self.d)

        self.midpointX = (
            self.midpoint(*self.lineDA),
            self.midpoint(*self.lineBC)
        )
        self.midpointY = (
            self.midpoint(*self.lineAB),
            self.midpoint(*self.lineCD)
        )

        self.quadrants = self.get_quadrants()
        self.holes = self.get_holes()

    def midpoint(self, a: tuple, b: tuple) -> tuple:
        '''
        Calcula o ponto médio de uma reta

        Parâmetros
        ----------

        a: tuple
            Ponto inicial da reta

        b: tuple
            Ponto final da reta

        Retorno
        -------
        tuple
            Ponto médio da reta

        Exemplos
        -------
        >>> midpoint((0, 0), (10, 10))
        (5, 5)
        '''
        return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)

    def get_quadrants(self) -> list:
        '''
        Retorna os quadrantes da peça de acordo com os cantos

        Retorno
        -------
        list
            Lista com os quadrantes
        '''
        return [
            [
                (self.midpoint(*self.lineAB), self.b),
                (self.b, self.midpoint(*self.lineBC))
            ],
            [
                (self.a, self.midpoint(*self.lineAB)),
                (self.a, self.midpoint(*self.lineDA))
            ],
            [
                (self.d, self.midpoint(*self.lineCD)),
                (self.midpoint(*self.lineDA), self.d)
            ],
            [
                (self.midpoint(*self.lineCD), self.c),
                (self.midpoint(*self.lineBC), self.c)
            ]
        ]

    def percentage_to_point(
        self,
        percentage: float,
        a: tuple,
        b: tuple
    ) -> tuple:
        '''
        Retorna um ponto percentual de uma reta

        Parâmetros
        ----------
        percentage: float
            Posição em porcentagem da reta

        a: tuple
            Ponto inicial da reta

        b: tuple
            Ponto final da reta

        Retorno
        -------
        tuple
            Ponto percentual da reta

        Exemplos
        -------
        >>> percentage_to_point(0.5, (0, 0), (10, 10))
        (5, 5)
        '''
        xdiff = (b[0] - a[0])
        ydiff = (b[1] - a[1])

        x = a[0] + (xdiff * percentage)
        y = a[1] + (ydiff * percentage)

        return (x, y)

    def linear_distance(self, a: tuple, b: tuple) -> tuple:
        '''
        Calcula a distância linear entre dois pontos em X e em Y

        Parâmetros
        ----------
        a: tuple
            Ponto inicial

        b: tuple
            Ponto final

        Retorno
        -------
        tuple
            Distância em X e em Y entre os pontos

        Exemplos
        -------
        >>> linear_distance((0, 0), (10, 15))
        (10, 15)
        '''
        x1, y1 = a
        x2, y2 = b

        return (x2 - x1, y2 - y1)

    def percentage_to_size(self, percentage: float, quadrant: int) -> int:
        '''
        Calcula um tamanho em porcentagem de acordo com o quadrante

        Parâmetros
        ----------
        percentage: float
            Porcentagem do tamanho

        quadrant: int
            Quadrante

        Retorno
        -------
        int
            Tamanho em porcentagem do quadrante
        '''
        point = self.get_point(quadrant, percentage, 0)
        distance = self.linear_distance(point, self.quadrants[quadrant][0][0])
        return distance[0]

    def line_intersection(self, line1: tuple, line2: tuple) -> tuple:
        '''
        Calcula a interseção entre duas retas

        Parâmetros
        ----------

        line1: tuple
            Reta 1

        line2: tuple
            Reta 2

        Retorno
        -------
        tuple
            Ponto de interseção entre as retas

        Exemplos
        -------
        >>> line_intersection(((0, 0), (10, 10)), ((0, 10), (10, 0)))
        (5, 5)
        '''
        xdiff = (
            self.linear_distance(*line1)[0],
            self.linear_distance(*line2)[0]
        )
        ydiff = (
            self.linear_distance(*line1)[1],
            self.linear_distance(*line2)[1]
        )

        def det(a, b):
            return a[1] * b[0] - a[0] * b[1]

        div = det(xdiff, ydiff)
        if div == 0:
            return 0, 0

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    def get_horizontal_parallel(
        self,
        distance,
        line_init,
        line_end
    ):
        x1, y1 = line_init
        x2, y2 = line_end

        init_x = x1
        end_x = x2

        init_y = y1 + distance
        end_y = y2 + distance

        line = ((int(init_x), int(init_y)), (int(end_x), int(end_y)))

        if self.pencil:
            cv.line(self.draw, *line, color=(128, 14, 241))

        return line

    def get_vertical_parallel(
        self,
        distance,
        line_init,
        line_end
    ):
        '''
        Get a vertical parallel line
        '''
        x1, y1 = line_init
        x2, y2 = line_end

        init_x = x1 + distance
        end_x = x2 + distance

        init_y = y1
        end_y = y2

        return ((init_x, init_y), (end_x, end_y))

    def check_horizontal_parallel(
        self,
        line1: tuple,
        line2: tuple
    ) -> bool:
        '''
        Verifica se duas retas são paralelas horizontalmente

        Parâmetros
        ----------
        line1: tuple
            Reta 1

        line2: tuple
            Reta 2

        Retorno
        -------
        bool
            Se as retas são paralelas horizontalmente

        Exemplos
        -------
        >>> check_horizontal_parallel(((0, 0), (10, 10)), ((0, 10), (10, 0)))
        False
        '''
        y11 = line1[0][1]
        y12 = line1[1][1]

        y21 = line2[0][1]
        y22 = line2[1][1]

        initial_distance = abs(y11 - y21)
        final_distance = abs(y12 - y22)

        return self.proximity(initial_distance, final_distance)

    def check_vertical_parallel(
        self, line1: tuple, line2: tuple
    ) -> bool:
        '''
        Verifica se duas retas são paralelas verticalmente

        Parâmetros
        ----------
        line1: tuple
            Reta 1

        line2: tuple
            Reta 2

        Retorno
        -------
        bool
            Se as retas são paralelas verticalmente

        Exemplos
        -------
        >>> check_vertical_parallel(((0, 0), (10, 10)), ((0, 10), (10, 0)))
        False
        '''
        x11 = line1[0][0]
        x12 = line1[1][0]

        x21 = line2[0][0]
        x22 = line2[1][0]

        initial_distance = abs(x11 - x21)
        final_distance = abs(x12 - x22)

        return self.proximity(initial_distance, final_distance)

    def get_point(
        self,
        quadrant: int,
        xpercentage: float,
        ypercentage: float
    ) -> tuple:

        x_point = self.percentage_to_point(
            xpercentage,
            *self.quadrants[quadrant][0]
        )
        y_point = self.percentage_to_point(
            ypercentage,
            *self.quadrants[quadrant][1]
        )

        horizontal_distance = 0
        vertical_distance = 0

        if quadrant in [0, 1]:
            horizontal_distance = self.linear_distance(
                self.quadrants[quadrant][1][0],
                y_point
            )[1]
        else:
            horizontal_distance = self.linear_distance(
                self.quadrants[quadrant][1][1],
                y_point
            )[1]

        if quadrant in [0, 3]:
            vertical_distance = self.linear_distance(
                self.quadrants[quadrant][0][1],
                x_point
            )[0]
        else:
            vertical_distance = self.linear_distance(
                self.quadrants[quadrant][0][0],
                x_point
            )[0]

        x_parallel = self.get_horizontal_parallel(
            horizontal_distance,
            *self.quadrants[quadrant][0]
        )

        y_parallel = self.get_vertical_parallel(
            vertical_distance,
            *self.quadrants[quadrant][1]
        )

        result_mid = self.line_intersection(x_parallel, y_parallel)

        if self.pencil:
            x11 = int(x_parallel[0][0])
            x12 = int(x_parallel[0][1])
            x21 = int(x_parallel[1][0])
            x22 = int(x_parallel[1][1])

            y11 = int(y_parallel[0][0])
            y12 = int(y_parallel[0][1])
            y21 = int(y_parallel[1][0])
            y22 = int(y_parallel[1][1])

            cv.line(self.draw, (x11, x12), (x21, x22), color=(128, 14, 241))
            cv.line(self.draw, (y11, y12), (y21, y22), color=(128, 14, 241))

        return result_mid

    def get_holes(self):
        holes = []
        for hole in self.part.holes:
            x, y = hole.position
            x, y = self.get_point(hole.quadrant, x, y)
            pos = {
                'quadrant': 0,
                'x': x,
                'y': y
            }
            current = Hole(hole.hole_type, pos, hole.size, hole.tolerance)
            holes.append(current)

        return holes

    def evaluate_holes(self):
        right = []
        for hole in self.holes:
            x = int(hole.position[0])
            y = int(hole.position[1])
            hole_size = hole.size + (hole.size*(hole.tolerance+0.2))
            size = abs(self.percentage_to_size(hole_size, hole.quadrant))
            x1 = int(x - size/2)
            y1 = int(y - size/2)
            x2 = int(x + size/2)
            y2 = int(y + size/2)

            crop = self.image[y1:y2, x1:x2]
            crop = cv.resize(crop, (240, 240))

            pred = predict_hole_type(crop)

            right_hole = pred == hole.hole_type

            if right_hole:
                right.append(crop)
            else:
                print(f'Wrong hole type. Expected {hole.hole_type} got {pred}')

            if self.pencil:
                color = (0, 255, 0) if right_hole else (0, 0, 255)
                cv.rectangle(self.draw, (x1, y1), (x2, y2), color, 2)
                cv.imshow(f'{self.part.name}', self.draw)

            cv.imshow(f'{hole.hole_type}', crop)

            key = cv.waitKey(30)
            if key == ord('q'):
                exit()

        return len(right) == len(self.holes)

    def draw_quadrants(self, color=(128, 14, 241)):
        for quadrant in self.quadrants:
            c111 = int(quadrant[0][0][0])
            c112 = int(quadrant[0][0][1])
            c121 = int(quadrant[0][1][0])
            c122 = int(quadrant[0][1][1])
            c211 = int(quadrant[1][0][0])
            c212 = int(quadrant[1][0][1])
            c221 = int(quadrant[1][1][0])
            c222 = int(quadrant[1][1][1])
            cv.line(self.draw, (c111, c112), (c121, c122), color=color, thickness=2)
            cv.line(self.draw, (c211, c212), (c221, c222), color=color, thickness=2)

            for points in quadrant:
                for point in points:
                    font = cv.FONT_HERSHEY_SIMPLEX
                    x = int(point[0])
                    y = int(point[1])
                    cv.putText(
                        self.draw,
                        'X',
                        (x, y),
                        font,
                        fontScale=0.5,
                        color=color
                    )

    def draw_center(self, color=(128, 14, 241)):
        m111 = int(self.midpointX[0][0])
        m112 = int(self.midpointX[0][1])
        m121 = int(self.midpointX[1][0])
        m122 = int(self.midpointX[1][1])
        m211 = int(self.midpointY[0][0])
        m212 = int(self.midpointY[0][1])
        m221 = int(self.midpointY[1][0])
        m222 = int(self.midpointY[1][1])

        cv.line(self.draw, (m111, m112), (m121, m122), color=color, thickness=2)
        cv.line(self.draw, (m211, m212), (m221, m222), color=color, thickness=2)

    def rotate_triangle(self, triangle: tuple) -> tuple:
        last_x = triangle[0]
        last_y = triangle[1]

        height, width, _ = self.image.shape

        x = width - last_y
        y = last_x

        return x, y

    def rotate_part(self):
        self.draw = self.image.copy()
        self.image = cv.rotate(self.image, cv.ROTATE_90_CLOCKWISE)
        self.draw = cv.rotate(self.draw, cv.ROTATE_90_CLOCKWISE)

        self.a = self.rotate_triangle(self.a)
        self.b = self.rotate_triangle(self.b)
        self.c = self.rotate_triangle(self.c)
        self.d = self.rotate_triangle(self.d)

        a, b, c, d = self.a, self.b, self.c, self.d

        self.a = d
        self.b = a
        self.c = b
        self.d = c

        self.calcule_all()

    def show(self):
        cv.imshow(f'{self.part.name}', self.draw)
        key = cv.waitKey(30)
        if key == ord('q'):
            exit()

    def close(self):
        cv.destroyWindow(f'{self.part.name}')
        cv.destroyWindow('circular')
        cv.destroyWindow('hexagonal')
        cv.destroyWindow('cross')
