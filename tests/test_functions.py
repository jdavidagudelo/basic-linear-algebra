from unittest.case import TestCase
from functions import Variable, Constant, Product, Sum, Power
import math


class MatrixTest(TestCase):
    evaluate_values = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 29992.209992, 100, -11, -12, 0,
                       -12.092, math.pi, math.e]
    constant_values = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 29992.209992, 100, -11, -12, 0,
                       -12.092, math.pi, math.e]
    evaluate_powers = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 11.209992, 10, -11, -12, 0,
                       -12.092, math.pi, math.e]

    variable_names = ['x', 'y', 'z', 'myVar', 'my_var']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_evaluate_variable_function(self):
        variable_function = Variable('x')
        for value in self.evaluate_values:
            self.assertEqual(value, variable_function.evaluate(value))

    def test_evaluate_constant_function(self):
        for constant_value in self.constant_values:
            constant_function = Constant(constant_value)
            for value in self.evaluate_values:
                self.assertEqual(constant_value, constant_function.evaluate(value))

    def test_print_variable_function(self):
        for variable_name in self.variable_names:
            variable_function = Variable(variable_name)
            self.assertEqual('{0}'.format(variable_function), variable_name)

    def test_print_constant_function(self):
        for constant_value in self.constant_values:
            constant_function = Constant(constant_value)
            self.assertEqual('{0}'.format(constant_value), '{0}'.format(constant_function))

    def test_derivative_constant_function(self):
        for constant_value in self.constant_values:
            constant_function = Constant(constant_value)
            zero_constant = Constant.zero()
            self.assertEqual(zero_constant, constant_function.derivative())

    def test_derivative_variable_function(self):
        for variable_name in self.variable_names:
            variable_function = Variable(variable_name)
            one_constant = Constant.one()
            self.assertEqual(one_constant, variable_function.derivative())

    def test_evaluate_product_function(self):
        for constant_value in self.constant_values:
            for second_constant_value in self.constant_values:
                product = Product([Constant(constant_value), Constant(second_constant_value)])
                for value in self.evaluate_values:
                    self.assertEqual(product.evaluate(value), constant_value * second_constant_value)
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    product = Product([Constant(constant_value), Variable(variable_name),
                                       Constant(second_constant_value)])
                    for value in self.evaluate_values:
                        self.assertEqual(product.evaluate(value), value * constant_value * second_constant_value)

    def test_print_product_function(self):
        for constant_value in self.constant_values:
            product = Product([Constant(constant_value)])
            self.assertEqual('{0}'.format(product), '{0}'.format(constant_value))
            for second_constant_value in self.constant_values:
                product = Product([Constant(constant_value), Constant(second_constant_value)])
                self.assertEqual('{0}'.format(product), '{0}*{1}'.format(constant_value,
                                                                         second_constant_value))
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                product = Product([Variable(variable_name)])
                self.assertEqual('{0}'.format(product), '{0}'.format(variable_name))
                for second_constant_value in self.constant_values:
                    product = Product([Constant(constant_value), Variable(variable_name),
                                       Constant(second_constant_value)])
                    self.assertEqual('{0}'.format(product), '{0}*{1}*{2}'.format(constant_value, variable_name,
                                                                                 second_constant_value))

    def test_simplify_product(self):
        for constant_value in self.constant_values:
            for second_constant_value in self.constant_values:
                product = Product([Constant(constant_value), Constant(second_constant_value)])
                simplified = product.simplify()
                self.assertEqual(simplified, Constant(constant_value * second_constant_value))
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    product = Product([Constant(constant_value), Variable(variable_name),
                                       Constant(second_constant_value)])
                    simplified = product.simplify()
                    if constant_value != 0.0 and second_constant_value != 0.0:
                        if constant_value * second_constant_value != 1.0:
                            self.assertEqual(simplified, Product([Constant(constant_value * second_constant_value),
                                                                  Variable(variable_name)]))
                        else:
                            self.assertEqual(simplified, Variable(variable_name))
                    else:
                        self.assertEqual(simplified, Constant.zero())
        for variable_name in self.variable_names:
            product_squared = Product([Variable(variable_name), Variable(variable_name)])
            self.assertEqual(product_squared.simplify(), Power(Variable(variable_name), 2))
            product_squared = Product([Variable(variable_name), Variable(variable_name), Variable(variable_name)])
            self.assertEqual(product_squared.simplify(), Power(Variable(variable_name), 3))
            product_squared = Product([Variable(variable_name), Variable(variable_name),
                                       Variable(variable_name), Variable(variable_name)])
            self.assertEqual(product_squared.simplify(), Power(Variable(variable_name), 4))

    def test_evaluate_sum_function(self):
        for constant_value in self.constant_values:
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                for value in self.evaluate_values:
                    self.assertEqual(sum_result.evaluate(value), constant_value + second_constant_value)
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    for value in self.evaluate_values:
                        self.assertEqual(sum_result.evaluate(value), value + constant_value + second_constant_value)

    def test_print_sum_function(self):
        for constant_value in self.constant_values:
            sum_result = Sum([Constant(constant_value)])
            self.assertEqual('{0}'.format(sum_result), '{0}'.format(constant_value))
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                self.assertEqual('{0}'.format(sum_result), '{0}+{1}'.format(constant_value,
                                                                            second_constant_value))
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                sum_result = Sum([Variable(variable_name)])
                self.assertEqual('{0}'.format(sum_result), '{0}'.format(variable_name))
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    self.assertEqual('{0}'.format(sum_result), '{0}+{1}+{2}'.format(constant_value, variable_name,
                                                                                    second_constant_value))

    def test_simplify_sum(self):
        for constant_value in self.constant_values:
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                simplified = sum_result.simplify()
                print(sum_result)
                print('result = {0}'.format(simplified))
                self.assertEqual(simplified, Constant(constant_value + second_constant_value))
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    simplified = sum_result.simplify()
                    if constant_value + second_constant_value != 0.0:
                        self.assertEqual(simplified, Sum([Constant(constant_value + second_constant_value),
                                                          Variable(variable_name)]))
                    else:
                        self.assertEqual(simplified, Variable(variable_name))
                    product_sum = Sum([Constant(constant_value),
                                      Product([Constant(second_constant_value),
                                               Constant(constant_value), Variable(variable_name)])])
                    simplified = product_sum.simplify()
                    print('{0} Simplified'.format(simplified))
                    print('{0} Original'.format(product_sum))
                    if constant_value != 0.0 and constant_value*second_constant_value != 1.0 and constant_value*second_constant_value != 0.0:
                        self.assertEqual(simplified, Sum([Constant(constant_value),
                                                          Product(
                                                              [Constant(constant_value*second_constant_value),
                                                               Variable(variable_name)])]))
                    elif constant_value*second_constant_value == 1.0:
                        self.assertEqual(simplified, Sum([Constant(constant_value), Variable(variable_name)]))
                    elif constant_value*second_constant_value == 0.0:
                        self.assertEqual(simplified, Constant(constant_value))
                    else:
                        self.assertEqual(simplified, Product([Constant(constant_value*second_constant_value),
                                                              Variable(variable_name)]))

    def test_derivative_sum_function(self):
        for constant_value in self.constant_values:
            sum_result = Sum([Constant(constant_value)])
            self.assertEqual(sum_result.derivative(), Constant.zero())
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                self.assertEqual(sum_result.derivative(), Constant.zero())
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                sum_result = Sum([Variable(variable_name)])
                self.assertEqual(sum_result.derivative(), Constant.one())
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    self.assertEqual(sum_result.derivative(), Constant.one())

    def test_derivative_product_function(self):
        for constant_value in self.constant_values:
            product = Product([Constant(constant_value)])
            self.assertEqual(product.derivative(), Constant.zero())
            for second_constant_value in self.constant_values:
                product = Product([Constant(constant_value), Constant(second_constant_value)])
                self.assertEqual(product.derivative(), Constant.zero())
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                product = Product([Variable(variable_name)])
                self.assertEqual(product.derivative(), Constant.one())
                for second_constant_value in self.constant_values:
                    product = Product([Constant(constant_value), Variable(variable_name),
                                       Constant(second_constant_value)])
                    self.assertEqual(product.derivative(), Constant(constant_value * second_constant_value))
        for variable_name in self.variable_names:
            product = Product([Variable(variable_name), Variable(variable_name)])
            self.assertEqual(product.derivative(), Product([Constant(2.0), Variable(variable_name)]))

    def test_polynomial_derivative(self):
        for variable_name in self.variable_names:
            for a1 in self.constant_values:
                for a2 in self.constant_values:
                    for a3 in self.constant_values:
                        polynomial = Sum(
                            [
                                Product([Constant(a1), Power(Variable(variable_name), 2)]),
                                Product([Constant(a2), Variable(variable_name)]),
                                Constant(a3)
                            ])
                        if a2 != 0:
                            expected = Sum([Constant(a2), Product([Constant(2*a1), Variable(variable_name)])])
                        else:
                            expected = Product([Constant(2*a1), Variable(variable_name)])
                        self.assertEqual(polynomial.derivative(),
                                         expected)

