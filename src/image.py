import cv2 as cv
from parts import Part
from holes import Hole


class PartImage:
    def __init__(
        self,
        image_path: str,
        triangles: list,
        part: Part,
        pencil: bool = False
    ):
        '''
        Construtor da classe PartImage

        Parâmetros
        ----------
        image_path: str
            Caminho da imagem

        triangles: list
            Lista de triângulos

        part: Part
            Peça a ser analisada

        pencil: bool
            Pincel de desenho
        '''
        self.pencil = pencil
        self.image_path = image_path
        self.image = cv.imread(image_path, 0)
        self.draw = cv.imread(image_path, 0)

        self.a, self.b, self.c, self.d = triangles

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
        self.part = part
        self.holes = self.get_holes()

    def midpoint(self, a: tuple, b: tuple) -> tuple:
        return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)

    def get_quadrants(self):
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

    def percentage_to_point(self, percentage, a, b):
        xdiff = (b[0] - a[0])
        ydiff = (b[1] - a[1])

        x = a[0] + (xdiff * percentage)
        y = a[1] + (ydiff * percentage)

        return (x, y)

    def linear_distance(self, a: tuple, b: tuple) -> tuple:
        x1, y1 = a
        x2, y2 = b

        return (x2 - x1, y2 - y1)

    def percentage_to_size(self, percentage, quadrant):
        point = self.get_point(quadrant, percentage, 0)
        distance = self.linear_distance(point, self.quadrants[quadrant][0][0])
        return distance[0]

    def line_intersection(self, line1, line2) -> tuple:
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
            cv.line(self.draw, *line, color=(255, 0, 0))

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

            cv.line(self.draw, (x11, x12), (x21, x22), color=(255, 0, 0))
            cv.line(self.draw, (y11, y12), (y21, y22), color=(255, 0, 0))

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

    def get_cropped_holes(self):
        cropped = []
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
            cropped.append(crop)

            if self.pencil:
                cv.rectangle(self.draw, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv.imshow(f'{self.part.name}', self.draw)

            cv.imshow(f'{hole.hole_type}', crop)
            key = cv.waitKey(0)
            if key == ord('q'):
                exit()

        return cropped

    def draw_quadrants(self, color=(255, 0, 0)):
        for quadrant in self.quadrants:
            c111 = int(quadrant[0][0][0])
            c112 = int(quadrant[0][0][1])
            c121 = int(quadrant[0][1][0])
            c122 = int(quadrant[0][1][1])
            c211 = int(quadrant[1][0][0])
            c212 = int(quadrant[1][0][1])
            c221 = int(quadrant[1][1][0])
            c222 = int(quadrant[1][1][1])
            cv.line(self.draw, (c111, c112), (c121, c122), color=color)
            cv.line(self.draw, (c211, c212), (c221, c222), color=color)

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
                        color=(255, 0, 0)
                    )

    def draw_center(self, color=(255, 0, 0)):
        m111 = int(self.midpointX[0][0])
        m112 = int(self.midpointX[0][1])
        m121 = int(self.midpointX[1][0])
        m122 = int(self.midpointX[1][1])
        m211 = int(self.midpointY[0][0])
        m212 = int(self.midpointY[0][1])
        m221 = int(self.midpointY[1][0])
        m222 = int(self.midpointY[1][1])

        cv.line(self.draw, (m111, m112), (m121, m122), color=color)
        cv.line(self.draw, (m211, m212), (m221, m222), color=color)

    def show(self):
        cv.imshow(f'{self.part.name}', self.draw)
        key = cv.waitKey(0)
        if key == ord('q'):
            exit()

    def close(self):
        cv.destroyAllWindows()
