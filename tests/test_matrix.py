from unittest.case import TestCase
from matrix import Matrix, Fraction

class MatrixTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_determinant_2dimensional_matrix(self):
        m = Matrix([[1, 2], [2, 3]])
        self.assertEqual(m.det(), -1)

    def test_determinant_3dimensional_matrix(self):
        m = Matrix([[2, 3, 4], [7, 8, 3], [4, 7, 8]])
        self.assertEqual(m.det(), 22)

    def test_determinant_4dimensional_matrix(self):
        m = Matrix([[1, 2, 3, 4], [4, 5, 8, 3], [7, 9, 1, 2], [7, 4, 2, 1]])
        self.assertEqual(m.det(), 727)

    def test_zero_determinant_matrix(self):
        m = Matrix([[1, 2], [8, 16]])
        self.assertEqual(m.det(), 0)

    def test_gauss_jordan_2dimensional_matrix(self):
        m = Matrix([[1, 2, 4], [2, 7, 8]])
        self.assertEqual(m.gauss_jordan_reduction().data, Matrix([[1, 0, 4], [0, 1, 0]]).data)

    def test_gauss_jordan_3dimensional_matrix(self):
        m = Matrix([[3, 7, 8, 2], [4, 5, 3, 4], [3, 2, 1, 7]])
        expected = [[1, 0, 0, 33/8], [0, 1, 0, -29/8], [0, 0, 1, 15/8]]
        result = m.gauss_jordan_reduction().data
        for i in range(m.m):
            for j in range(m.n):
                self.assertAlmostEqual(expected[i][j], result[i][j])

    def test_gauss_jordan_order_rows(self):
        m = Matrix([[0, 0, 1, 2], [1, 0, 0, 3], [0, 1, 0, 2]])
        self.assertEqual(m.gauss_jordan_reduction().data, [[1, 0, 0, 3], [0, 1, 0, 2], [0, 0, 1, 2]])

    def test_fraction_operations(self):
        f = Fraction(1, 2).add(Fraction(1, 3))
        self.assertEqual(f.numerator, 5)
        self.assertEqual(f.denominator, 6)
        f = Fraction(3, 5).multiply(Fraction(40, 25))
        self.assertEqual(f.numerator, 24)
        self.assertEqual(f.denominator, 25)
        f = Fraction(3, 5).divide(Fraction(25, 40))
        self.assertEqual(f.numerator, 24)
        self.assertEqual(f.denominator, 25)
        f = Fraction(1, 2).subtract(Fraction(1, 3))
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 6)
        f = Fraction(1020, 20).simplify()
        self.assertEqual(f.numerator, 51)
        self.assertEqual(f.denominator, 1)

    def test_inverse_matrix(self):
        m = Matrix([[1, 2], [3, 5]])
        self.assertEqual([[-5, 2], [3, -1]], m.inverse().data)
        self.assertEqual(m.inverse().multiply(m).data, [[1, 0], [0, 1]])

    def test_multiply_matrices(self):
        m = Matrix([[1, 3], [2, 7]]).multiply(Matrix([[2, 5, 8], [4, 3, 2]]))
        self.assertEqual(m.data, [[14, 14, 14], [32, 31, 30]])



