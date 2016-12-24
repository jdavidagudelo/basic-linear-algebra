
class InvalidMatrixDeterminantException(Exception):
    pass


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def mcm(a, b):
    return a * b / gcd(a, b)


class Fraction(object):
    numerator = None
    denominator = None

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.add(other)

    def __sub__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.subtract(other)

    def __mul__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.multiply(other)

    def __truediv__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.divide(other)

    def __neg__(self):
        return self.negate()

    def __float__(self):
        return float(self.numerator) / float(self.denominator)

    def __lt__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return float(self) < float(other)

    def __le__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return float(self) <= float(other)

    def __ge__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return float(self) >= float(other)

    def __gt__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return float(self) > float(other)

    def __ne__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.numerator != other.numerator or self.denominator != other.denominator

    def __eq__(self, other):
        if isinstance(other, (int,)):
            other = Fraction(other, 1)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def simplify(self):
        divisor = gcd(self.numerator, self.denominator)
        return Fraction(self.numerator/divisor, self.denominator/divisor)

    def add(self, other):
        denominator = mcm(self.denominator, other.denominator)
        numerator = denominator/self.denominator*self.numerator + denominator/other.denominator*other.numerator
        return Fraction(numerator, denominator).simplify()

    def negate(self):
        return Fraction(-self.numerator, self.denominator).simplify()

    def subtract(self, other):
        return self.add(other.negate())

    def multiply(self, other):
        return Fraction(self.numerator*other.numerator, self.denominator*other.denominator).simplify()

    def divide(self, other):
        return self.multiply(Fraction(other.denominator, other.numerator)).simplify()


class Matrix(object):
    data = []

    def __init__(self, data=None, m=None, n=None, data_type=None):
        n = 0 if n is None else n
        m = 0 if m is None else m
        self.data = data if data is not None else [[0 for _ in range(n)] for _ in range(m)]
        if data_type == Fraction:
            for i in range(0, self.m):
                for j in range(0, self.n):
                    if isinstance(self.data[i][j], int):
                        self.data[i][j] = Fraction(self.data[i][j], 1)

    def copy(self):
        result = Matrix(m=self.m, n=self.n)
        for i in range(0, self.m):
            for j in range(0, self.n):
                result.data[i][j] = self.data[i][j]
        return result

    @property
    def m(self):
        return len(self.data)

    @property
    def n(self):
        try:
            return len(self.data[0])
        except IndexError:
            return 0

    def remove_column(self, column):
        result = Matrix(m=self.m, n=self.n - 1)
        for i in range(0, self.m):
            for j in range(0, self.n):
                if j != column:
                    result.data[i][j if j < column else j - 1] = self.data[i][j]
        return result

    def remove_row(self, row):
        result = Matrix(m=self.m - 1, n=self.n)
        for i in range(0, self.m):
            if i != row:
                for j in range(0, self.n):
                    result.data[i if i < row else i - 1][j] = self.data[i][j]
        return result

    def leading_zeros(self, row):
        j = 0
        while j < self.n and self.data[row][j] == 0:
            j += 1
        return j

    def order_rows(self):
        for i in range(0, self.m):
            for k in range(i + 1, self.m):
                if self.leading_zeros(i) > self.leading_zeros(k):
                    aux = self.data[k]
                    self.data[k] = self.data[i]
                    self.data[i] = aux

    def inverse(self):
        result = Matrix(m=self.m, n=2*self.n)
        for i in range(0, self.m):
            result.data[i][i + self.n] = 1.0
        for i in range(0, self.m):
            for j in range(0, self.n):
                result.data[i][j] = self.data[i][j]
        complete = result.gauss_jordan_reduction()
        result = Matrix(m=self.m, n=self.n)
        for i in range(0, self.m):
            for j in range(self.n, 2*self.n):
                result.data[i][j - self.n] = complete.data[i][j]
        return result

    def multiply(self, other):
        result = Matrix(m=self.m, n=other.n)
        for i in range(0, self.m):
            for j in range(0, other.n):
                value = 0
                for k in range(0, self.n):
                    value += self.data[i][k] * other.data[k][j]
                result.data[i][j] = value
        return result

    def gauss_jordan_reduction(self):
        result = self.copy()
        result.order_rows()
        j = 0
        for i in range(0, result.m):
            current_pivot = result.data[i][j]
            if current_pivot != 1 and current_pivot != 0:
                for k in range(j, result.n):
                    result.data[i][k] /= current_pivot
            for k in range(result.m):
                if k != i:
                    if result.data[i][j] != 0 and result.data[k][j] != 0:
                        factor = result.data[k][j]/result.data[i][j]
                        for l in range(j, result.n):
                            result.data[k][l] -= factor * result.data[i][l]
            j += 1
        return result

    def __str__(self):
        return '{0}'.format(self.data)

    def det(self):
        if self.m != self.n:
            raise InvalidMatrixDeterminantException('The determinant operation is only valid for square matrices.')
        if self.m == self.n and self.m == 2:
            return self.data[0][0] * self.data[1][1] - self.data[1][0]*self.data[0][1]
        result = 0
        for i in range(self.n):
            result += self.data[0][i] * self.remove_row(0).remove_column(i).det() * (1 if (i % 2) == 0 else -1)
        return result
