from dm.coefficients.AbstractLineCoefficients import AbstractLineCoefficients


class CenterLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        a = point_y
        b = -point_x

        return -a / b

