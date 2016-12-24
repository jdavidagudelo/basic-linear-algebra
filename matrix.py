
class InvalidMatrixDeterminantException(Exception):
    pass


class Matrix(object):
    data = []

    def __init__(self, data=None, m=None, n=None):
        n = 0 if n is None else n
        m = 0 if m is None else m
        self.data = data if data is not None else [[0 for _ in range(n)] for _ in range(m)]

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

    def order_rows(self):
        for i in range(0, self.m):
            for k in range(i + 1, self.m):
                j1 = 0
                j2 = 0
                j = 0
                while j < self.n and self.data[i][j] == 0:
                    j1 += 1
                    j += 1
                j = 0
                while j < self.n and self.data[k][j] == 0:
                    j2 += 1
                    j += 1
                if j1 > j2:
                    aux = self.data[k]
                    self.data[k] = self.data[i]
                    self.data[i] = aux

    def gauss_jordan_reduction(self):
        result = self.copy()
        result.order_rows()
        j = 0
        for i in range(0, result.m):
            current_pivot = float(result.data[i][j])
            if current_pivot != 1.0 and current_pivot != 0.0:
                for k in range(j, result.n):
                    result.data[i][k] = float(result.data[i][k])/current_pivot
            for k in range(result.m):
                if k != i:
                    if result.data[i][j] != 0 and result.data[k][j] != 0:
                        factor = float(result.data[k][j])/float(result.data[i][j])
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
